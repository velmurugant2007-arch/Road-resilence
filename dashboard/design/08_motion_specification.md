# Deliverable 8: ATLAS Motion & Animation Specification

**Animation Engine:** Framer Motion (`framer-motion` v11+)  
**Core Rule:** All animations MUST be subtle, tactical, and functional. Flashy bouncing or distracting spring oscillations are strictly prohibited to maintain ISRO professional standards.

---

## 1. Spring & Easing Transition Presets

All Framer Motion transitions reference standardized spring physics configurations:

```ts
export const MOTION_PRESETS = {
  // Smooth HUD Expansion (Sidebar, Floating Panels)
  hudSpring: {
    type: "spring",
    stiffness: 260,
    damping: 28,
    mass: 0.8
  },
  // Snappy Micro-interactions (Buttons, Toggles, Tooltips)
  snappySpring: {
    type: "spring",
    stiffness: 400,
    damping: 30
  },
  // Gentle Fade & Scale (Modals, Dialogs)
  modalEase: {
    duration: 0.25,
    ease: [0.16, 1, 0.3, 1] // Apple custom cubic-bezier
  }
};
```

---

## 2. Specific Component Animation Recipes

### Sidebar Expansion (`SidebarNavigationDock`)
* **Trigger:** User hovers or clicks the expansion arrow.
* **Framer Motion Variant:**
  ```tsx
  const sidebarVariants = {
    collapsed: { width: "64px", transition: MOTION_PRESETS.hudSpring },
    expanded: { width: "220px", transition: MOTION_PRESETS.hudSpring }
  };
  ```

### Floating Inspector Panel Opening (`FloatingInspectorPanel`)
* **Trigger:** Selecting a healed edge or disaster priority item.
* **Framer Motion Variant:**
  ```tsx
  const panelVariants = {
    hidden: { opacity: 0, x: 40, scale: 0.98 },
    visible: { 
      opacity: 1, 
      x: 0, 
      scale: 1, 
      transition: MOTION_PRESETS.hudSpring 
    },
    exit: { opacity: 0, x: 20, transition: { duration: 0.15 } }
  };
  ```

### Card Hover Effect (`StatisticsCounterCard`)
* **Trigger:** Mouse hover over telemetry card.
* **Animation:** Subtle 2px elevation lift with specular border glow increase.
  ```tsx
  <motion.div
    whileHover={{ y: -2, borderColor: "rgba(0, 242, 254, 0.4)" }}
    transition={MOTION_PRESETS.snappySpring}
  />
  ```

### Animated Statistic Counters
* **Trigger:** Incoming telemetry data or simulation step increment.
* **Implementation:** Uses Framer Motion `useSpring` and `useTransform` hooked to a text node rendering inside a `Roboto Mono` span. Number ticks smoothly over 600ms without jittering adjacent layout elements.

### Healed Edge Map Pulse (Deck.gl Shader Animation)
* **Trigger:** Rendering accepted healed edges (`RH-###`).
* **WebGL Behavior:** Uniform time variable passed to custom fragment shader causes a soft cyan glow pulse (`0.3Hz`) traveling along the polyline vector.
