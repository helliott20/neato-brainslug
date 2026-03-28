import { LitElement, html, css } from "lit";
import { customElement, state, query } from "lit/decorators.js";
import { entityStore } from "./entity-store";
import { LidarButton, LidarSensor, LidarBinarySensor, TextSensor } from "./neato-enums";
import { pressButton } from "./api";

interface LidarPoint {
  angle: number;
  dist: number;
  intensity: number;
}

@customElement("lidar-map")
export class LidarMap extends LitElement {
  @state() scanning = false;
  @state() quality = 0;
  @state() nearestDist = 0;
  @state() nearestAngle = 0;

  @query("#lidar-canvas")
  canvas!: HTMLCanvasElement;

  private points: LidarPoint[] = [];
  private scale = 15; // pixels per 100mm
  private offsetX = 0;
  private offsetY = 0;
  private isDragging = false;
  private lastMouseX = 0;
  private lastMouseY = 0;
  private animFrameId = 0;
  private logicalWidth = 500;
  private logicalHeight = 500;
  private _unsubscribe?: () => void;

  static styles = css`
    :host {
      display: block;
      width: 100%;
    }

    .lidar-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 1rem;
    }

    .controls {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
      justify-content: center;
    }

    .controls button {
      padding: 0.5rem 1rem;
      border: 1px solid rgba(127, 127, 127, 0.5);
      border-radius: 0.5rem;
      background: rgba(127, 127, 127, 0.15);
      color: inherit;
      cursor: pointer;
      font-size: 0.9rem;
    }

    .controls button:hover {
      background: rgba(127, 127, 127, 0.3);
    }

    .controls button.active {
      background: rgba(0, 150, 255, 0.3);
      border-color: rgba(0, 150, 255, 0.6);
    }

    .stats {
      display: flex;
      gap: 1.5rem;
      font-size: 0.85rem;
      opacity: 0.8;
    }

    canvas {
      border: 1px solid rgba(127, 127, 127, 0.3);
      border-radius: 0.5rem;
      cursor: grab;
      max-width: 100%;
      touch-action: none;
    }

    canvas:active {
      cursor: grabbing;
    }

    .hint {
      font-size: 0.8rem;
      opacity: 0.6;
      text-align: center;
    }
  `;

  connectedCallback() {
    super.connectedCallback();
    this._unsubscribe = entityStore.subscribe(() => this._onEntityUpdate());
  }

  disconnectedCallback() {
    super.disconnectedCallback();
    this._unsubscribe?.();
    if (this.animFrameId) cancelAnimationFrame(this.animFrameId);
  }

  private _onEntityUpdate() {
    const scanData = entityStore.get(TextSensor.lidar_scan_data);
    const scanning = entityStore.get(LidarBinarySensor.scanning);
    const quality = entityStore.get(LidarSensor.scan_quality);
    const nearest = entityStore.get(LidarSensor.nearest_dist);
    const angle = entityStore.get(LidarSensor.nearest_angle);

    if (scanning) this.scanning = scanning.state === "ON";
    if (quality) this.quality = parseFloat(quality.value) || 0;
    if (nearest) this.nearestDist = parseFloat(nearest.value) || 0;
    if (angle) this.nearestAngle = parseFloat(angle.value) || 0;

    if (scanData?.state && scanData.state !== "nan" && scanData.state.startsWith("[")) {
      try {
        const parsed: number[][] = JSON.parse(scanData.state);
        this.points = parsed.map(p => ({
          angle: p[0],
          dist: p[1],
          intensity: p[2],
        }));
        this._renderMap();
      } catch (e) {
        // Ignore parse errors
      }
    }
  }

  private _renderMap() {
    if (!this.canvas) return;
    const ctx = this.canvas.getContext("2d");
    if (!ctx) return;

    const w = this.logicalWidth;
    const h = this.logicalHeight;
    const cx = w / 2 + this.offsetX;
    const cy = h / 2 + this.offsetY;
    const isDark = getComputedStyle(document.documentElement).colorScheme === "dark"
      || window.matchMedia("(prefers-color-scheme: dark)").matches;

    // Clear
    ctx.fillStyle = isDark ? "#1a1a2e" : "#f5f5f5";
    ctx.fillRect(0, 0, w, h);

    // Draw grid rings (every 1 meter = 1000mm)
    ctx.strokeStyle = isDark ? "rgba(255,255,255,0.08)" : "rgba(0,0,0,0.08)";
    ctx.lineWidth = 1;
    for (let r = 1; r <= 6; r++) {
      const pr = (r * 1000 * this.scale) / 100;
      ctx.beginPath();
      ctx.arc(cx, cy, pr, 0, Math.PI * 2);
      ctx.stroke();

      // Label
      ctx.fillStyle = isDark ? "rgba(255,255,255,0.3)" : "rgba(0,0,0,0.3)";
      ctx.font = "10px monospace";
      ctx.fillText(`${r}m`, cx + pr + 3, cy - 3);
    }

    // Draw crosshair
    ctx.strokeStyle = isDark ? "rgba(255,255,255,0.15)" : "rgba(0,0,0,0.15)";
    ctx.beginPath();
    ctx.moveTo(cx - 15, cy);
    ctx.lineTo(cx + 15, cy);
    ctx.moveTo(cx, cy - 15);
    ctx.lineTo(cx, cy + 15);
    ctx.stroke();

    // Draw robot triangle
    ctx.fillStyle = isDark ? "#00c853" : "#2e7d32";
    ctx.beginPath();
    ctx.moveTo(cx, cy - 8);
    ctx.lineTo(cx - 6, cy + 6);
    ctx.lineTo(cx + 6, cy + 6);
    ctx.closePath();
    ctx.fill();

    // Draw LIDAR points
    if (this.points.length === 0) {
      ctx.fillStyle = isDark ? "rgba(255,255,255,0.4)" : "rgba(0,0,0,0.4)";
      ctx.font = "14px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("No scan data. Press 'Single Scan' to start.", cx, cy + 40);
      ctx.textAlign = "start";
      return;
    }

    // Find max intensity for normalization
    const maxIntensity = this.points.reduce((m, p) => Math.max(m, p.intensity), 1);

    for (const point of this.points) {
      const rad = ((point.angle - 90) * Math.PI) / 180; // -90 to put 0° at top
      const px = cx + (point.dist * this.scale / 100) * Math.cos(rad);
      const py = cy + (point.dist * this.scale / 100) * Math.sin(rad);

      const alpha = 0.4 + 0.6 * (point.intensity / maxIntensity);
      ctx.fillStyle = isDark
        ? `rgba(64, 196, 255, ${alpha})`
        : `rgba(21, 101, 192, ${alpha})`;
      ctx.fillRect(px - 1.5, py - 1.5, 3, 3);
    }

    // Draw nearest obstacle indicator
    if (this.nearestDist > 0) {
      const nearRad = ((this.nearestAngle - 90) * Math.PI) / 180;
      const nx = cx + (this.nearestDist * this.scale / 100) * Math.cos(nearRad);
      const ny = cy + (this.nearestDist * this.scale / 100) * Math.sin(nearRad);
      ctx.strokeStyle = isDark ? "#ff5252" : "#d32f2f";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(nx, ny, 6, 0, Math.PI * 2);
      ctx.stroke();
    }
  }

  private _onWheel(e: WheelEvent) {
    e.preventDefault();
    const delta = e.deltaY > 0 ? -1 : 1;
    this.scale = Math.max(2, Math.min(50, this.scale + delta));
    this._renderMap();
  }

  private _onPointerDown(e: PointerEvent) {
    this.isDragging = true;
    this.lastMouseX = e.clientX;
    this.lastMouseY = e.clientY;
    (e.target as HTMLElement).setPointerCapture(e.pointerId);
  }

  private _onPointerMove(e: PointerEvent) {
    if (!this.isDragging) return;
    this.offsetX += e.clientX - this.lastMouseX;
    this.offsetY += e.clientY - this.lastMouseY;
    this.lastMouseX = e.clientX;
    this.lastMouseY = e.clientY;
    this._renderMap();
  }

  private _onPointerUp() {
    this.isDragging = false;
  }

  private _resetView() {
    this.offsetX = 0;
    this.offsetY = 0;
    this.scale = 15;
    this._renderMap();
  }

  private _doSingleScan() {
    const entity = entityStore.get(LidarButton.lidar_scan);
    if (entity) pressButton(entity);
  }

  private _doContinuousScan() {
    const entity = entityStore.get(LidarButton.lidar_scan_continuous);
    if (entity) pressButton(entity);
  }

  private _doStopScan() {
    const entity = entityStore.get(LidarButton.lidar_stop);
    if (entity) pressButton(entity);
  }

  firstUpdated() {
    if (this.canvas) {
      const dpr = window.devicePixelRatio || 1;
      const rect = this.canvas.getBoundingClientRect();
      this.logicalWidth = rect.width || 500;
      this.logicalHeight = rect.height || 500;
      this.canvas.width = this.logicalWidth * dpr;
      this.canvas.height = this.logicalHeight * dpr;
      const ctx = this.canvas.getContext("2d");
      if (ctx) ctx.scale(dpr, dpr);

      this.canvas.style.width = this.logicalWidth + "px";
      this.canvas.style.height = this.logicalHeight + "px";
    }
    this._renderMap();
  }

  render() {
    return html`
      <div class="lidar-container">
        <div class="controls">
          <button @click="${this._doSingleScan}">Single Scan</button>
          <button
            class="${this.scanning ? "active" : ""}"
            @click="${this.scanning ? this._doStopScan : this._doContinuousScan}"
          >
            ${this.scanning ? "Stop Scanning" : "Continuous Scan"}
          </button>
          <button @click="${this._resetView}">Reset View</button>
        </div>

        <div class="stats">
          <span>Quality: ${this.quality}%</span>
          <span>Points: ${this.points.length}</span>
          <span>Nearest: ${this.nearestDist > 0 ? `${this.nearestDist}mm @ ${this.nearestAngle}°` : "—"}</span>
        </div>

        <canvas
          id="lidar-canvas"
          width="500"
          height="500"
          style="width:500px;height:500px"
          @wheel="${this._onWheel}"
          @pointerdown="${this._onPointerDown}"
          @pointermove="${this._onPointerMove}"
          @pointerup="${this._onPointerUp}"
          @pointercancel="${this._onPointerUp}"
        ></canvas>

        <div class="hint">Scroll to zoom · Drag to pan</div>
      </div>
    `;
  }
}
