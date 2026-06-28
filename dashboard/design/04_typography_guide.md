# Deliverable 4: ATLAS Professional Typography Guide

**Font Families:** `Outfit` (Headings/Display), `Inter` (Body/UI Labels), `Roboto Mono` (Telemetry/Coordinates/Numbers)  
**Philosophy:** Clear hierarchical contrast with monospace alignment for numerical precision during disaster simulation.  

---

## 1. Font Family Stack

```css
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Outfit:wght@500;600;700&family=Roboto+Mono:wght@400;500;600&display=swap');

:root {
  --font-display: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-body: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'Roboto Mono', monospace;
}
```

---

## 2. Type Scale & Hierarchy Tokens

All line heights and sizes are calibrated to ensure crisp legibility inside translucent glass cards.

| Role | Font Family | Size | Weight | Line Height | Letter Spacing | Example Application |
| :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **Display / Page Title** | `Outfit` | 24px (1.5rem) | 700 (Bold) | 1.2 | `-0.02em` | Active Page Title ("Graph Healing HUD") |
| **Section Header (H2)** | `Outfit` | 18px (1.125rem)| 600 (Semi) | 1.3 | `-0.01em` | Panel Section Header ("Hybrid Cost Weights") |
| **Card Title (H3)** | `Inter` | 14px (0.875rem)| 600 (Semi) | 1.4 | `0.0em` | Stat Card Header ("Global Network Efficiency") |
| **Body Regular** | `Inter` | 13px (0.8125rem)|400 (Regular)|1.5| `0.0em` | XAI Repair Explanations, descriptive text |
| **Small UI Label / Caption**|`Inter`| 11px (0.6875rem)|500 (Medium)|1.3| `0.05em` | Table column headers, badge labels (UPPERCASE) |
| **Metric Value (Large)** | `Roboto Mono`| 28px (1.75rem)| 600 (Semi) | 1.1 | `-0.03em` | Counter displays ("84.2%", "50ms") |
| **Coordinate / Telemetry**| `Roboto Mono`| 12px (0.75rem) | 400 (Regular)|1.4| `0.0em` | Lat/Lon coordinates ("12.9140° N, 77.5201° E") |

---

## 3. Typography Color Hierarchy

To avoid visual fatigue on dark themes, absolute white (`#FFFFFF`) is reserved strictly for active headers and highlighted data counters. Body text uses softened opacities.

```css
:root {
  --text-primary: #FFFFFF;              /* 100% white for headings & active numbers */
  --text-secondary: rgba(255,255,255,0.70); /* 70% white for body readability */
  --text-tertiary: rgba(255,255,255,0.45);  /* 45% white for timestamps & inactive labels */
  --text-disabled: rgba(255,255,255,0.25);  /* 25% white for disabled controls */
}
```

---

## 4. Numerical Tabular Alignment

When displaying live simulation statistics or criticality tables, all numerical characters MUST use `font-variant-numeric: tabular-nums;`. This prevents visual jitter when counters tick upward or downward during Framer Motion playback.
