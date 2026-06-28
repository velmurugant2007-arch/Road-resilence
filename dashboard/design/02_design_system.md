# Deliverable 2: ATLAS Design System Tokens & Aesthetics

**Design Language:** Deep Space Obsidian (ISRO Premium Dark Mode)  
**Inspiration:** Apple HIG, Linear.app, Vercel Geists, Tesla Telemetry  

---

## 1. Aesthetic Principles & Glassmorphism Guidelines

To achieve an ISRO-grade tactical feel, the interface relies on deep obsidian backgrounds contrasted against glowing neon data vectors and translucent frosted glass panels.

### The Glassmorphism Recipe (Floating HUD Panels):
* **Background:** `rgba(13, 17, 23, 0.72)` (Dark obsidian with 72% opacity)
* **Backdrop Blur:** `backdrop-filter: blur(20px) saturate(180%)`
* **Border:** `1px solid rgba(255, 255, 255, 0.08)` (Subtle specular highlights)
* **Inner Glow (Top Edge):** `box-shadow: inset 0 1px 0 0 rgba(255, 255, 255, 0.12)`
* **Drop Shadow:** `0 20px 40px -15px rgba(0, 0, 0, 0.7)`

### Soft Neumorphism (Tactical Hardware Buttons ONLY):
Neumorphism is restricted exclusively to primary execution triggers (e.g., "EXECUTE HEALING", "SIMULATE BLAST") to mimic physical space-command hardware toggles.
* **Raised State:** `background: linear-gradient(135deg, #1f2937, #111827); box-shadow: -4px -4px 10px rgba(255,255,255,0.04), 4px 4px 12px rgba(0,0,0,0.6);`
* **Pressed / Active State:** `box-shadow: inset 2px 2px 5px rgba(0,0,0,0.8), inset -1px -1px 3px rgba(255,255,255,0.05);`

---

## 2. Spacing Scale (8pt Grid System)

All component dimensions, margins, and padding adhere strictly to an 8pt spatial cadence (with 4pt half-steps for compact data rows).

| Token | Size (px) | Rem | Application |
| :--- | :---: | :---: | :--- |
| `--space-1` | 4px | 0.25rem | Icon gaps, tight badge padding, border widths |
| `--space-2` | 8px | 0.5rem | Button padding (vertical), list item spacing |
| `--space-3` | 12px | 0.75rem | Compact HUD padding, form input gutters |
| `--space-4` | 16px | 1.0rem | Standard card padding, HUD panel margins |
| `--space-6` | 24px | 1.5rem | Section spacing, floating dock offsets |
| `--space-8` | 32px | 2.0rem | Major panel separations, top HUD height padding |
| `--space-12` | 48px | 3.0rem | Screen edge gutters for wide displays |

---

## 3. Border Radius Tokens

Corner curvature is designed to feel sleek and highly engineered.

| Token | Value | Application |
| :--- | :---: | :--- |
| `--radius-sm` | 4px | Badges, tooltips, inline code blocks |
| `--radius-md` | 8px | Interactive buttons, dropdown menus, input fields |
| `--radius-lg` | 14px | Floating inspector panels, statistic cards, dialogs |
| `--radius-xl` | 20px | Outer HUD docks, floating command bars |
| `--radius-full`| 9999px | Status indicators, user avatars, pill toggles |

---

## 4. Shadow & Elevation Tokens

Shadows define visual elevation above the 70% map canvas.

```css
:root {
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.4);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -1px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.6), 0 4px 6px -2px rgba(0, 0, 0, 0.4);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.7), 0 10px 10px -5px rgba(0, 0, 0, 0.5);
  --shadow-hud: 0 25px 50px -12px rgba(0, 0, 0, 0.85), 0 0 20px rgba(0, 242, 254, 0.15);
}
```

---

## 5. Blur & Opacity Tokens

```css
:root {
  --blur-xs: blur(4px);
  --blur-sm: blur(8px);
  --blur-md: blur(16px);
  --blur-lg: blur(24px);
  --blur-xl: blur(40px);
  
  --opacity-surface: 0.72;
  --opacity-surface-hover: 0.85;
  --opacity-surface-active: 0.95;
  --opacity-border: 0.12;
}
```
