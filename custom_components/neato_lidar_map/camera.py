"""Camera platform for Neato LIDAR Map."""
from __future__ import annotations

import io
import json
import logging
import math

from PIL import Image, ImageDraw, ImageFont

from homeassistant.components.camera import Camera
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import (
    CONF_IMAGE_SIZE,
    CONF_LIDAR_ENTITY,
    CONF_MAX_RANGE,
    CONF_POS_X_ENTITY,
    CONF_POS_Y_ENTITY,
    CONF_POS_HEADING_ENTITY,
    DEFAULT_IMAGE_SIZE,
    DEFAULT_MAX_RANGE,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Neato LIDAR Map camera."""
    config = hass.data[DOMAIN][config_entry.entry_id]

    async_add_entities(
        [NeatoLidarCamera(hass, config_entry, config)],
        update_before_add=True,
    )


class NeatoLidarCamera(Camera):
    """Representation of a Neato LIDAR Map camera."""

    _attr_has_entity_name = True
    _attr_name = "LIDAR Map"
    _attr_is_streaming = False

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        config: dict,
    ) -> None:
        """Initialize the camera."""
        super().__init__()
        self._hass = hass
        self._config_entry = config_entry
        self._lidar_entity_id = config[CONF_LIDAR_ENTITY]
        self._pos_x_entity_id = config.get(CONF_POS_X_ENTITY)
        self._pos_y_entity_id = config.get(CONF_POS_Y_ENTITY)
        self._pos_heading_entity_id = config.get(CONF_POS_HEADING_ENTITY)
        self._image_size = config.get(CONF_IMAGE_SIZE, DEFAULT_IMAGE_SIZE)
        self._max_range = config.get(CONF_MAX_RANGE, DEFAULT_MAX_RANGE)
        self._image_bytes: bytes | None = None
        self._scan_data: list[list[int]] = []
        # Accumulated map points from multiple scans with position data
        # Each entry: (world_x_mm, world_y_mm, intensity)
        self._map_points: list[tuple[float, float, int]] = []
        self._cleaning_path: list[tuple[float, float]] = []
        self._max_accumulated = 10000  # cap accumulated points

        self._attr_unique_id = f"{config_entry.entry_id}_lidar_map"

    async def async_added_to_hass(self) -> None:
        """Run when entity is added to hass."""
        await super().async_added_to_hass()

        # Pre-render placeholder off the event loop
        self._image_bytes = await self._hass.async_add_executor_job(
            self._render_placeholder
        )

        # Listen for LIDAR scan data changes
        self.async_on_remove(
            async_track_state_change_event(
                self._hass,
                [self._lidar_entity_id],
                self._handle_lidar_update,
            )
        )

        # Render initial state
        state = self._hass.states.get(self._lidar_entity_id)
        if state and state.state not in ("unknown", "unavailable", ""):
            await self._process_scan_data(state.state)

    @callback
    def _handle_lidar_update(self, event) -> None:
        """Handle LIDAR data update."""
        new_state = event.data.get("new_state")
        if new_state is None:
            return

        state_val = new_state.state
        if state_val in ("unknown", "unavailable", ""):
            return

        self._hass.async_create_task(self._process_scan_data(state_val))

    def _get_robot_position(self) -> tuple[float, float, float] | None:
        """Get current robot position from HA entities."""
        if not all([self._pos_x_entity_id, self._pos_y_entity_id]):
            return None

        x_state = self._hass.states.get(self._pos_x_entity_id)
        y_state = self._hass.states.get(self._pos_y_entity_id)

        if not x_state or not y_state:
            return None
        if x_state.state in ("unknown", "unavailable"):
            return None
        if y_state.state in ("unknown", "unavailable"):
            return None

        heading = 0.0
        if self._pos_heading_entity_id:
            h_state = self._hass.states.get(self._pos_heading_entity_id)
            if h_state and h_state.state not in ("unknown", "unavailable"):
                try:
                    heading = float(h_state.state)
                except ValueError:
                    pass

        try:
            return (float(x_state.state), float(y_state.state), heading)
        except ValueError:
            return None

    async def _process_scan_data(self, state_val: str) -> None:
        """Process scan data and render image."""
        try:
            scan_data = json.loads(state_val)
            if not isinstance(scan_data, list):
                return
            self._scan_data = scan_data

            # If we have position data, accumulate world-space points
            pos = self._get_robot_position()
            if pos is not None:
                robot_x, robot_y, heading = pos
                heading_rad = math.radians(heading)

                # Record cleaning path
                self._cleaning_path.append((robot_x, robot_y))
                if len(self._cleaning_path) > 5000:
                    self._cleaning_path = self._cleaning_path[-5000:]

                # Transform scan points to world coordinates
                for point in scan_data:
                    if len(point) < 3:
                        continue
                    angle_deg, dist_mm, intensity = point[0], point[1], point[2]
                    if dist_mm <= 0:
                        continue

                    # Robot-relative angle to world angle
                    world_angle = math.radians(angle_deg) + heading_rad
                    world_x = robot_x + dist_mm * math.cos(world_angle)
                    world_y = robot_y + dist_mm * math.sin(world_angle)
                    self._map_points.append((world_x, world_y, intensity))

                # Cap accumulated points
                if len(self._map_points) > self._max_accumulated:
                    self._map_points = self._map_points[-self._max_accumulated:]

                self._image_bytes = await self._hass.async_add_executor_job(
                    self._render_accumulated_map
                )
            else:
                # No position data - render single scan view
                self._image_bytes = await self._hass.async_add_executor_job(
                    self._render_map, scan_data
                )

            self.async_write_ha_state()
        except (json.JSONDecodeError, TypeError, ValueError):
            _LOGGER.debug("Failed to parse LIDAR scan data")

    def _render_map(self, scan_data: list[list[int]]) -> bytes:
        """Render LIDAR scan data as a PNG image."""
        size = self._image_size
        max_range = self._max_range

        # Create image with dark background
        img = Image.new("RGB", (size, size), (26, 26, 46))
        draw = ImageDraw.Draw(img)

        cx = size // 2
        cy = size // 2
        scale = (size / 2 - 20) / max_range  # pixels per mm

        # Draw grid rings every 1 meter (subtle dark grey)
        for r in range(1, 7):
            radius = int(r * 1000 * scale)
            if radius > size // 2:
                break
            draw.ellipse(
                [cx - radius, cy - radius, cx + radius, cy + radius],
                outline=(45, 45, 65),
                width=1,
            )

        # Draw crosshair
        draw.line([(cx - 10, cy), (cx + 10, cy)], fill=(55, 55, 75), width=1)
        draw.line([(cx, cy - 10), (cx, cy + 10)], fill=(55, 55, 75), width=1)

        # Draw LIDAR points
        nearest_dist = 99999
        nearest_px = 0
        nearest_py = 0

        max_intensity = max((p[2] for p in scan_data if len(p) >= 3), default=1)
        if max_intensity == 0:
            max_intensity = 1

        for point in scan_data:
            if len(point) < 3:
                continue
            angle_deg, dist_mm, intensity = point[0], point[1], point[2]

            if dist_mm <= 0:
                continue

            rad = math.radians(angle_deg - 90)  # 0° at top
            px = cx + int(dist_mm * scale * math.cos(rad))
            py = cy + int(dist_mm * scale * math.sin(rad))

            # Intensity-based brightness (brighter = stronger signal)
            brightness = 0.4 + 0.6 * (intensity / max_intensity)
            color = (
                int(64 * brightness),
                int(196 * brightness),
                int(255 * brightness),
            )

            # Draw 3x3 pixel dot
            draw.rectangle([px - 1, py - 1, px + 1, py + 1], fill=color)

            if dist_mm < nearest_dist:
                nearest_dist = dist_mm
                nearest_px = px
                nearest_py = py

        # Draw robot (green triangle at center)
        robot_points = [
            (cx, cy - 8),
            (cx - 6, cy + 6),
            (cx + 6, cy + 6),
        ]
        draw.polygon(robot_points, fill=(0, 200, 83))

        # Draw nearest obstacle indicator (red circle)
        if nearest_dist < 99999:
            draw.ellipse(
                [nearest_px - 5, nearest_py - 5, nearest_px + 5, nearest_py + 5],
                outline=(255, 82, 82),
                width=2,
            )

        # Add stats text
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None
        stats = f"Points: {len(scan_data)} | Range: {max_range / 1000:.0f}m"
        if nearest_dist < 99999:
            stats += f" | Nearest: {nearest_dist}mm"
        draw.text((5, size - 15), stats, fill=(180, 180, 180), font=font)

        # Convert to PNG bytes
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        return buf.getvalue()

    def _render_accumulated_map(self) -> bytes:
        """Render accumulated map from multiple positioned scans."""
        size = self._image_size
        img = Image.new("RGB", (size, size), (26, 26, 46))
        draw = ImageDraw.Draw(img)

        if not self._map_points:
            return self._render_placeholder()

        # Find bounding box of all points
        all_x = [p[0] for p in self._map_points]
        all_y = [p[1] for p in self._map_points]
        if self._cleaning_path:
            all_x.extend(p[0] for p in self._cleaning_path)
            all_y.extend(p[1] for p in self._cleaning_path)

        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)

        # Add margin
        margin = 500  # 500mm margin
        min_x -= margin
        min_y -= margin
        max_x += margin
        max_y += margin

        range_x = max_x - min_x
        range_y = max_y - min_y
        if range_x == 0:
            range_x = 1
        if range_y == 0:
            range_y = 1

        # Scale to fit image
        scale = min((size - 20) / range_x, (size - 20) / range_y)

        def to_px(wx: float, wy: float) -> tuple[int, int]:
            px = int(10 + (wx - min_x) * scale)
            py = int(size - 10 - (wy - min_y) * scale)  # flip Y
            return (px, py)

        # Draw grid (1m intervals)
        grid_start_x = int(min_x / 1000) * 1000
        grid_start_y = int(min_y / 1000) * 1000
        for gx in range(grid_start_x, int(max_x) + 1000, 1000):
            px1 = to_px(gx, min_y)
            px2 = to_px(gx, max_y)
            draw.line([px1, px2], fill=(45, 45, 65), width=1)
        for gy in range(grid_start_y, int(max_y) + 1000, 1000):
            px1 = to_px(min_x, gy)
            px2 = to_px(max_x, gy)
            draw.line([px1, px2], fill=(45, 45, 65), width=1)

        # Draw cleaning path
        if len(self._cleaning_path) >= 2:
            path_pixels = [to_px(p[0], p[1]) for p in self._cleaning_path]
            draw.line(path_pixels, fill=(0, 100, 200), width=1)

        # Draw accumulated scan points
        max_intensity = max((p[2] for p in self._map_points), default=1)
        if max_intensity == 0:
            max_intensity = 1
        for wx, wy, intensity in self._map_points:
            px, py = to_px(wx, wy)
            if 0 <= px < size and 0 <= py < size:
                brightness = 0.4 + 0.6 * (intensity / max_intensity)
                color = (
                    int(64 * brightness),
                    int(196 * brightness),
                    int(255 * brightness),
                )
                draw.rectangle([px - 1, py - 1, px + 1, py + 1], fill=color)

        # Draw robot current position
        pos = self._get_robot_position()
        if pos is not None:
            rpx, rpy = to_px(pos[0], pos[1])
            # Green dot for robot
            draw.ellipse(
                [rpx - 5, rpy - 5, rpx + 5, rpy + 5],
                fill=(0, 200, 83),
            )

        # Stats
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None
        stats = f"Points: {len(self._map_points)} | Path: {len(self._cleaning_path)} steps"
        draw.text((5, size - 15), stats, fill=(180, 180, 180), font=font)

        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        return buf.getvalue()

    def camera_image(
        self, width: int | None = None, height: int | None = None
    ) -> bytes | None:
        """Return the current LIDAR map image."""
        return self._image_bytes

    def _render_placeholder(self) -> bytes:
        """Render a placeholder image when no data is available."""
        size = self._image_size
        img = Image.new("RGB", (size, size), (26, 26, 46))
        draw = ImageDraw.Draw(img)
        cx, cy = size // 2, size // 2

        text1 = "No LIDAR data available"
        text2 = "Trigger a scan from brainslug"
        bbox1 = draw.textbbox((0, 0), text1)
        bbox2 = draw.textbbox((0, 0), text2)
        w1 = bbox1[2] - bbox1[0]
        w2 = bbox2[2] - bbox2[0]

        draw.text((cx - w1 // 2, cy), text1, fill=(150, 150, 150))
        draw.text((cx - w2 // 2, cy + 20), text2, fill=(100, 100, 100))

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        return buf.getvalue()

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra state attributes."""
        attrs = {
            "scan_points": len(self._scan_data),
            "accumulated_points": len(self._map_points),
            "path_steps": len(self._cleaning_path),
            "image_size": self._image_size,
            "max_range_mm": self._max_range,
        }

        if self._scan_data:
            distances = [p[1] for p in self._scan_data if len(p) >= 2 and p[1] > 0]
            if distances:
                attrs["nearest_obstacle_mm"] = min(distances)
                attrs["farthest_reading_mm"] = max(distances)

        pos = self._get_robot_position()
        if pos is not None:
            attrs["robot_x_mm"] = pos[0]
            attrs["robot_y_mm"] = pos[1]
            attrs["robot_heading_deg"] = pos[2]

        return attrs
