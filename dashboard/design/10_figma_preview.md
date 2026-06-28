# Deliverable 10: ATLAS Figma-Style UI Visual Mockups

This document provides high-fidelity inline SVG and structured Markdown previews illustrating the visual appearance of the ATLAS dashboard before React code implementation.

---

## 1. High-Fidelity Dashboard Interface Mockup (SVG Preview)

The following inline SVG renders the layout proportions, glassmorphic styling, neon data vector glow, and floating HUD overlays.

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" width="100%" height="100%" style="background:#05070A; font-family:'Inter', sans-serif;">
  <!-- Base Satellite Map Canvas (Dark Matter Representation) -->
  <rect width="1440" height="900" fill="#0A0E14" />
  
  <!-- Simulated Grid Lines & Urban Blocks -->
  <path d="M 0 200 L 1440 200 M 0 450 L 1440 450 M 0 700 L 1440 700 M 300 0 L 300 900 M 700 0 L 700 900 M 1100 0 L 1100 900" stroke="#1E293B" stroke-width="1" stroke-dasharray="4 4" />
  
  <!-- Baseline Road Polylines (Neon Cyan Glow) -->
  <path d="M 100 800 L 350 600 L 600 650 L 850 400 L 1200 350" stroke="#00F2FE" stroke-width="4" fill="none" filter="drop-shadow(0 0 8px #00F2FE)" />
  <path d="M 350 600 L 400 300 L 750 200" stroke="#00F2FE" stroke-width="3" fill="none" opacity="0.8" />
  
  <!-- Cloud Occlusion Mask (Translucent Purple Overlay) -->
  <ellipse cx="650" cy="500" rx="140" ry="90" fill="url(#cloudGrad)" opacity="0.65" />
  <defs>
    <radialGradient id="cloudGrad" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#E100FF" stop-opacity="0.8" />
      <stop offset="100%" stop-color="#7F00FF" stop-opacity="0" />
    </radialGradient>
  </defs>
  
  <!-- Healed Road Repair Pulse (Accepted XAI Link) -->
  <path d="M 600 650 L 750 380" stroke="#10B981" stroke-width="3" stroke-dasharray="8 6" fill="none" filter="drop-shadow(0 0 10px #10B981)" />
  <circle cx="675" cy="515" r="8" fill="#10B981" />
  <text x="695" y="520" fill="#10B981" font-size="12" font-weight="bold">RH-001 [ACC]</text>

  <!-- TOP TELEMETRY HUD BAR (Glassmorphism) -->
  <rect x="24" y="20" width="1392" height="56" rx="14" fill="#0F172A" fill-opacity="0.75" stroke="#FFFFFF" stroke-opacity="0.15" stroke-width="1" />
  <text x="50" y="54" fill="#FFFFFF" font-family="'Outfit', sans-serif" font-size="18" font-weight="bold" letter-spacing="1">ATLAS</text>
  <text x="120" y="53" fill="#00F2FE" font-size="13" font-weight="600">ISRO ROUTE RESILIENCE COMMAND</text>
  
  <!-- Health Pill -->
  <rect x="650" y="32" width="140" height="32" rx="16" fill="#003B46" stroke="#00F2FE" stroke-width="1" />
  <circle cx="670" cy="48" r="4" fill="#00F2FE" />
  <text x="685" y="52" fill="#FFFFFF" font-size="12" font-weight="bold">API: HEALTHY</text>
  
  <!-- LEFT SIDEBAR DOCK (Collapsed 64px) -->
  <rect x="24" y="96" width="64" height="700" rx="20" fill="#0F172A" fill-opacity="0.75" stroke="#FFFFFF" stroke-opacity="0.12" stroke-width="1" />
  <!-- Nav Icons -->
  <circle cx="56" cy="140" r="16" fill="#00F2FE" fill-opacity="0.2" />
  <circle cx="56" cy="140" r="6" fill="#00F2FE" />
  <circle cx="56" cy="200" r="6" fill="#64748B" />
  <circle cx="56" cy="260" r="6" fill="#64748B" />
  <circle cx="56" cy="320" r="6" fill="#64748B" />
  <circle cx="56" cy="380" r="6" fill="#64748B" />

  <!-- RIGHT FLOATING INSPECTOR PANEL (Explainability XAI Viewer) -->
  <rect x="1056" y="96" width="360" height="700" rx="16" fill="#0F172A" fill-opacity="0.82" stroke="#FFFFFF" stroke-opacity="0.18" stroke-width="1" filter="drop-shadow(0 20px 30px rgba(0,0,0,0.8))" />
  <text x="1080" y="135" fill="#FFFFFF" font-family="'Outfit', sans-serif" font-size="16" font-weight="bold">XAI REPAIR INSPECTOR</text>
  <path d="M 1080 150 L 1392 150" stroke="#FFFFFF" stroke-opacity="0.1" stroke-width="1" />
  
  <!-- Edge ID & Badge -->
  <text x="1080" y="185" fill="#94A3B8" font-size="12">Selected Link Candidate</text>
  <text x="1080" y="210" fill="#FFFFFF" font-family="'Roboto Mono', monospace" font-size="20" font-weight="bold">ID: RH-001</text>
  <rect x="1290" y="192" width="100" height="24" rx="12" fill="#10B981" fill-opacity="0.2" stroke="#10B981" stroke-width="1" />
  <text x="1308" y="208" fill="#10B981" font-size="11" font-weight="bold">ACCEPTED</text>
  
  <!-- Score Bars -->
  <text x="1080" y="255" fill="#E2E8F0" font-size="13">AI Confidence Map</text>
  <text x="1355" y="255" fill="#00F2FE" font-family="'Roboto Mono', monospace" font-size="13">0.91</text>
  <rect x="1080" y="265" width="312" height="6" rx="3" fill="#334155" />
  <rect x="1080" y="265" width="283" height="6" rx="3" fill="#00F2FE" />

  <text x="1080" y="305" fill="#E2E8F0" font-size="13">Direction Consistency</text>
  <text x="1355" y="305" fill="#00F2FE" font-family="'Roboto Mono', monospace" font-size="13">0.96</text>
  <rect x="1080" y="315" width="312" height="6" rx="3" fill="#334155" />
  <rect x="1080" y="315" width="300" height="6" rx="3" fill="#00F2FE" />

  <text x="1080" y="355" fill="#E2E8F0" font-size="13">Road Width Similarity</text>
  <text x="1355" y="355" fill="#00F2FE" font-family="'Roboto Mono', monospace" font-size="13">0.88</text>
  <rect x="1080" y="365" width="312" height="6" rx="3" fill="#334155" />
  <rect x="1080" y="365" width="274" height="6" rx="3" fill="#00F2FE" />
  
  <!-- Hybrid Score Circle -->
  <circle cx="1236" cy="450" r="45" fill="#1E293B" stroke="#00F2FE" stroke-width="4" filter="drop-shadow(0 0 10px rgba(0,242,254,0.3))" />
  <text x="1215" y="455" fill="#FFFFFF" font-family="'Roboto Mono', monospace" font-size="20" font-weight="bold">0.93</text>
  <text x="1205" y="520" fill="#94A3B8" font-size="12">Hybrid Cost Score</text>

  <!-- Explanation Rationale Callout -->
  <rect x="1080" y="550" width="312" height="100" rx="8" fill="#1E293B" fill-opacity="0.6" stroke="#FFFFFF" stroke-opacity="0.1" stroke-width="1" />
  <text x="1095" y="575" fill="#10B981" font-size="12" font-weight="bold">AI Rationale:</text>
  <text x="1095" y="600" fill="#CBD5E1" font-size="12">Accepted because the AI confidence (0.91)</text>
  <text x="1095" y="620" fill="#CBD5E1" font-size="12">exceeded threshold (0.65) and directional</text>
  <text x="1095" y="640" fill="#CBD5E1" font-size="12">consistency confirmed road alignment.</text>
  
  <!-- BOTTOM SIMULATION TIMELINE HUD -->
  <rect x="350" y="810" width="650" height="64" rx="32" fill="#0F172A" fill-opacity="0.85" stroke="#FFFFFF" stroke-opacity="0.15" stroke-width="1" />
  <circle cx="395" cy="842" r="18" fill="#00F2FE" />
  <polygon points="391,835 391,849 403,842" fill="#000000" />
  <text x="435" y="847" fill="#FFFFFF" font-family="'Roboto Mono', monospace" font-size="14" font-weight="bold">STEP 3 / 10</text>
  <!-- Timeline Scrubbing Track -->
  <rect x="540" y="840" width="420" height="4" rx="2" fill="#334155" />
  <rect x="540" y="840" width="126" height="4" rx="2" fill="#EF4444" />
  <circle cx="666" cy="842" r="8" fill="#FFFFFF" stroke="#EF4444" stroke-width="2" />
</svg>
```

---

## 2. Component Layout Breakdown (Figma Component Specifications)

### A. Explainability Card Component Specification
* **Padding:** `24px` (`--space-6`)
* **Background:** Frosted glass `--surface-1` with `20px` backdrop blur.
* **Header Typography:** `Outfit` Bold 16px.
* **Badge:** `Radius-full`, `10px` vertical padding, `100%` width alignment on small viewports.

### B. Navigation Dock Specification
* **Collapsed Width:** `64px`
* **Expanded Width:** `220px`
* **Transition:** `Framer Motion type: spring, stiffness: 260, damping: 28`
* **Active Icon Indicator:** `24px` vertical neon pill anchored to left border of active nav item.
