# LIDAR Map & No-Go Zones Setup Guide

This guide covers setting up the LIDAR visualization and no-go zone features for Neato D3-D7 (Gen3) robots using neato-brainslug.

## What You Get

- **Live LIDAR scanning** - See what your robot sees (360-degree scan)
- **LIDAR map in Home Assistant** - Camera entity showing the scan as an image
- **No-go zones** - Define zones and the robot state is tracked
- **Web UI visualization** - Interactive LIDAR map in the brainslug web interface

## Prerequisites

- Neato D3/D5/D7 (Gen3) robot with ESP32 installed and brainslug working
- Home Assistant with ESPHome integration configured
- LIDAR-enabled brainslug firmware (this fork)

## Step 1: Flash the Updated Firmware

### Using ESPHome Dashboard (recommended)

1. Copy the updated `config/gen3.yaml` to your ESPHome config directory
2. The key changes from stock brainslug:
   - Increased UART RX buffer to 8192 bytes (needed for LIDAR scan data)
   - Added `GetLDSScan` UART command parsing
   - Added LIDAR sensors, buttons, and text sensors
   - Added no-go zone globals with persistent storage
3. Flash via ESPHome Dashboard as normal

### Using your existing brainslug YAML

If you have a customized YAML, add these changes to your existing config:

**1. Increase UART buffer** (required - LIDAR scans are ~7KB):
```yaml
uart:
  rx_buffer_size: 8192  # was 2048
```

**2. Add LIDAR globals** - see the `globals:` section in gen3.yaml for:
- `g_lidar_scan_json`
- `g_lidar_scanning`
- `g_lidar_scan_quality`
- `g_lidar_nearest_dist`
- `g_lidar_nearest_angle`
- `g_nogo_zones` (with `restore_value: yes`)

**3. Add LIDAR scripts** - `lidar_scan`, `lidar_scan_continuous`, `lidar_stop`

**4. Add LIDAR parser** - see the `GetLDSScan` section in the UART debug lambda

**5. Add sensors/buttons** - LIDAR scan quality, nearest distance/angle, scan buttons

## Step 2: Install the HA Custom Integration

The custom integration renders LIDAR scan data as a camera entity in Home Assistant.

### Manual Installation

1. Copy the `custom_components/neato_lidar_map/` folder to your Home Assistant `config/custom_components/` directory:

```
config/
  custom_components/
    neato_lidar_map/
      __init__.py
      camera.py
      config_flow.py
      const.py
      manifest.json
      strings.json
```

2. Restart Home Assistant

3. Go to **Settings > Devices & Services > Add Integration**

4. Search for **"Neato LIDAR Map"**

5. Configure:
   - **LIDAR Scan Data entity**: Select `sensor.neato_vacuum_lidar_scan_data` (the text sensor from your brainslug device)
   - **Image size**: 600 (default, increase for higher resolution)
   - **Max range**: 5000mm (5 meters, adjust based on your room sizes)

6. A new camera entity `camera.neato_lidar_map_lidar_map` will be created

## Step 3: Add Dashboard Cards

### Simple Map Card

Add a **Picture Entity** card to your dashboard:
- Entity: `camera.neato_lidar_map_lidar_map`
- Camera view: Auto

### Full Control Panel

See `config/home-assistant/gen3-lidar-card.yaml` for a complete card configuration with:
- LIDAR map image
- Scan control buttons (single scan, continuous, stop)
- LIDAR statistics (quality, nearest obstacle)

## Step 4: Using LIDAR Scan

### From the Web UI
1. Open your brainslug web interface (usually `http://neato-vacuum.local`)
2. Scroll to the **LIDAR Map** section
3. Click **Single Scan** for a one-time scan
4. Click **Continuous Scan** for live updating (1 scan/second)
5. Scroll to zoom, drag to pan

### From Home Assistant
1. Press the **LIDAR Scan** button entity
2. The camera entity will update with the rendered map
3. For continuous scanning, press **LIDAR Scan Continuous**
4. Press **LIDAR Stop** to stop continuous scanning

### From HA Automations
```yaml
# Trigger a LIDAR scan
service: esphome.neato_vacuum_lidar_scan
data: {}

# Start continuous scanning
service: esphome.neato_vacuum_lidar_scan_continuous
data: {}

# Stop scanning
service: esphome.neato_vacuum_lidar_stop
data: {}
```

## Step 5: No-Go Zones

### Setting Zones via Home Assistant

No-go zones are stored as a JSON array on the ESP32 and persist across reboots.

**Zone format:**
```json
[
  {
    "name": "Kitchen",
    "x1": -1000, "y1": -500,
    "x2": 500, "y2": 500,
    "enabled": true
  }
]
```

Coordinates are in millimeters relative to the robot's initial position.

**Set zones via HA service call:**
```yaml
service: esphome.neato_vacuum_set_nogo_zones
data:
  zones_json: '[{"name":"Kitchen","x1":-1000,"y1":-500,"x2":500,"y2":500,"enabled":true}]'
```

**Set zones via the web UI:**
Use the No-Go Zones Config text entity to paste a JSON zone definition.

### Current Limitations

- **No automatic enforcement yet** - Zone enforcement requires robot position tracking, which depends on pose data from the robot. The D7's serial interface provides limited position data during cleaning.
- **Zones are rectangular** - Defined by two corner points (x1,y1) and (x2,y2)
- **Coordinates are relative** - Based on LIDAR scan coordinates, not absolute room positions
- **Zone drawing UI** - Currently set via JSON. A graphical zone drawing tool on the LIDAR map is planned.

## Troubleshooting

### No LIDAR data showing
1. Check that the ESP32 is connected to the robot and communicating (other commands like GetCharger should work)
2. Check ESPHome logs for `[lidar]` messages
3. The LIDAR motor must be running - it spins up when the robot is awake
4. If the robot is asleep/docked, wake it first (press any button on the robot)

### LIDAR scan quality is low
- Some angles may have no readings due to obstructions or the robot's own body
- Quality of 70-90% is normal
- Very low quality (<50%) may indicate the LIDAR sensor needs cleaning

### Camera entity not updating
1. Verify the LIDAR Scan Data text sensor has data (check its state in Developer Tools)
2. Restart the Neato LIDAR Map integration
3. Check HA logs for errors from `neato_lidar_map`

### ESP32 memory issues
- The LIDAR scan uses ~14KB of RAM on the ESP32
- If you see OOM errors, try reducing other ESPHome components
- The Elegoo ESP32-WROOM-32 (4MB flash, 520KB SRAM) should have sufficient headroom

## Technical Details

### LIDAR Data Flow
```
Robot LIDAR sensor
    ↓ (GetLDSScan command via UART @ 115200 baud)
ESP32 (ESPHome)
    ↓ (parses 360 CSV lines → JSON array)
    ├── Web UI (SSE /events → canvas rendering)
    └── HA (ESPHome API → text sensor entity)
            ↓
        neato_lidar_map integration
            ↓ (renders PNG from JSON scan data)
        camera entity in HA dashboard
```

### GetLDSScan Response Format
```
GetLDSScan
AngleDeg,DistInMM,Intensity,ErrorCodeHEX
0,1234,8,0
1,1230,7,0
2,0,0,8035
...
359,1250,9,0
```

Each line: angle (0-359), distance in mm, signal intensity, error code (0 = valid).
