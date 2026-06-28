# Deliverable 9: ATLAS Dashboard Layout & Accessibility Specification

**Grid System:** 12-Column CSS Grid Overlay over 100% Viewport WebGL Map  
**Accessibility Standard:** WCAG 2.1 AA Compliant (High Contrast & Keyboard Navigable)  

---

## 1. Spatial Layout Budget (70/30 Rule)

```text
+-----------------------------------------------------------------------------------+
| Top HUD Telemetry Bar (Height: 56px, Fixed Top Anchor, Z-Index: 400)               |
+-----+--------------------------------------------------------------------+--------+
|     |                                                                    |        |
|  S  |                                                                    |   F    |
|  I  |                                                                    |   L    |
|  D  |                                                                    |   O    |
|  E  |                                                                    |   A    |
|     |                    WEBGL MAP CANVAS (70% Footprint)                |   T    |
|  D  |                    Fully interactive spatial view                  |   I    |
|  O  |                    Pans, zooms, and rotates freely                 |   N    |
|  C  |                                                                    |   G    |
|  K  |                                                                    |        |
|     |                                                                    |   P    |
| (64 |                                                                    |   A    |
|  px)|                                                                    |   N    |
|     |                                                                    |   E    |
|  Z: |                                                                    |   L    |
| 400 |                                                                    | (360px)|
|     |                                                                    | Z: 500 |
+-----+--------------------------------------------------------------------+--------+
| Simulation Timeline HUD (Height: 72px, Bottom-Center Anchored, Z-Index: 400)      |
+-----------------------------------------------------------------------------------+
```

---

## 2. Responsive Layout Rules

### Desktop Monitors (1920x1080 & Above) - *Primary Target*
* Sidebar Dock is expanded or collapsed per user preference. Floating panel anchors to right edge with a 16px outer margin.
* Map canvas is unconstrained.

### Tablet / Compact Laptops (1024px to 1440px)
* Sidebar Dock forces collapsed state (64px width).
* Floating panel shrinks width to `320px` and overlays map controls.

### Mobile / Narrow Viewports (<768px) - *Secondary Diagnostic Mode*
* Floating HUD panels slide down to form a bottom sheet drawer (occupying bottom 45% of screen).
* Map canvas remains visible in top 55% of screen. Top Telemetry bar simplifies to Logo + Health Status pill.

---

## 3. Accessibility & Keyboard Navigation Specification

To support rapid command execution in emergency control rooms without requiring mouse precision:

### Keyboard Shortcuts (Command Palette Accessible via `Ctrl+K` / `Cmd+K`)
* `1` - `8`: Instant view switching across the 8 operational dashboard pages.
* `Space`: Play / Pause active disaster stress simulation.
* `R`: Reset map view to default Hero City Bounding Box.
* `H`: Toggle visibility of all HUD overlays (pure 100% map fullscreen mode).
* `Esc`: Close active floating inspector panel or clear active road selection.

### High Contrast & Focus Indicators
* **Focus Ring:** Every interactive button, slider, and table row MUST outline with a `2px solid #00F2FE` neon cyan glow offset by `2px` when focused via `Tab` key.
* **Color Blindness Compatibility:** Critical network status badges never rely on color alone. Status pills include distinct geometric iconography:
  * `[✓] ACCEPTED` (Success Green)
  * `[!] WARNING` (Warning Amber)
  * `[✕] REJECTED` (Critical Red)
