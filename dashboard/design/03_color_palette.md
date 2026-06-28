# Deliverable 3: ATLAS Curated Color Palette

**Theme:** Deep Obsidian Tactical & Neon Cyan Data Glow  
**Color Standard:** HSL & Hexadecimal mapping tailored for high-contrast dark OLED screens.  

---

## 1. Primary & Secondary Brand Tokens

The primary color represents high-confidence AI predictions, baseline healthy network roads, and active UI highlights. The secondary color represents analytical computation and secondary graph structures.

| Token Name | Hex Code | HSL Value | Purpose & Application |
| :--- | :---: | :---: | :--- |
| `--primary-500` | `#00F2FE` | `hsla(183, 100%, 50%, 1)` | Active map roads, primary CTA buttons, active HUD icons |
| `--primary-400` | `#4FACFE` | `hsla(208, 99%, 65%, 1)` | Hover states, glowing polyline borders |
| `--primary-900` | `#003B46` | `hsla(189, 100%, 14%, 0.4)` | Subdued badge backgrounds, active list selection rows |
| `--secondary-500`| `#7F00FF` | `hsla(270, 100%, 50%, 1)` | AI segmentation masks, analytical processing indicators |
| `--secondary-400`| `#E100FF` | `hsla(293, 100%, 50%, 1)` | AI occlusion boundaries, XAI attention highlights |

---

## 2. Functional & Tactical State Colors

Used strictly for geospatial status reporting, graph criticality ranking, and disaster simulations.

| State | Hex Code | HSL Value | Spatial & UI Application |
| :--- | :---: | :---: | :--- |
| **Success (Healthy)** | `#10B981` | `hsla(158, 84%, 39%, 1)` | Repaired road gaps accepted by XAI, system operational status |
| **Warning (Degraded)** | `#F59E0B` | `hsla(38, 92%, 50%, 1)` | Moderate centrality bottlenecks (0.4 - 0.6), low AI confidence warnings |
| **Critical (Failure)** | `#EF4444` | `hsla(0, 84%, 60%, 1)` | Severed disaster bridges, severed articulation points, rejected healing candidates |
| **Info (Neutral)** | `#3B82F6` | `hsla(217, 91%, 60%, 1)` | Baseline node markers, general system telemetry logs |

---

## 3. Background, Surface & Border Scale

Designed to ensure absolute legibility against dark satellite imagery.

```css
:root, [data-theme="dark"] {
  /* Canvas Backgrounds */
  --bg-canvas: #05070A;          /* Deepest cosmic black for empty map regions */
  --bg-app: #0A0E14;             /* Main app wrapper background */
  
  /* Glassmorphic Surfaces */
  --surface-1: rgba(15, 23, 42, 0.65);  /* Floating HUD base panels */
  --surface-2: rgba(30, 41, 59, 0.75);  /* Hovered cards, active tabs */
  --surface-3: rgba(51, 65, 85, 0.85);  /* Dialog modals, elevated popovers */
  
  /* Borders & Dividers */
  --border-subtle: rgba(255, 255, 255, 0.08); /* Card outlines */
  --border-strong: rgba(255, 255, 255, 0.18); /* Active input borders, focused elements */
  --border-glow: rgba(0, 242, 254, 0.50);     /* Selected road segment highlight border */
}

[data-theme="light"] {
  --bg-canvas: #F8FAFC;
  --bg-app: #F1F5F9;
  --surface-1: rgba(255, 255, 255, 0.75);
  --surface-2: rgba(241, 245, 249, 0.85);
  --surface-3: rgba(226, 232, 240, 0.95);
  --border-subtle: rgba(0, 0, 0, 0.08);
  --border-strong: rgba(0, 0, 0, 0.18);
  --border-glow: rgba(0, 140, 255, 0.50);
}
```

---

## 4. Map Palette Mapping (Deck.gl / Mapbox GL)

When rendering vector data over CartoDB Dark Matter tiles, exact HEX values are passed to GPU color buffers:

```json
{
  "map_layers": {
    "baseline_roads": [0, 242, 254, 200],
    "healed_repairs_accepted": [16, 185, 129, 255],
    "healed_repairs_rejected": [239, 68, 68, 150],
    "critical_bottleneck_roads": [255, 0, 85, 255],
    "disaster_blast_zone": [239, 68, 68, 60],
    "cloud_occlusion_mask": [225, 0, 255, 120]
  }
}
```
