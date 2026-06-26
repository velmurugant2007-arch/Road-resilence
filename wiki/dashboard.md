# Dashboard

## Project ATLAS — Route Resilience
### Knowledge Base Entry

> Dashboard design philosophy, visualization strategy, and interactive features. The dashboard is the primary demonstration interface for judges.

---

## Status

> ⚠️ Dashboard design begins in **Phase 5**. No technology stack decisions have been made.

## Design Philosophy

The dashboard must serve two audiences:
1. **Judges** — Quick visual impact, clear storytelling, interactive demo
2. **Engineers** — Detailed metrics, drill-down capability, diagnostic views

## Anticipated Visualization Layers

| Layer | Content | Interaction |
|---|---|---|
| Base Map | Satellite imagery with geographic context | Pan, zoom |
| Road Extraction | Segmentation overlay showing extracted roads | Toggle, opacity |
| Occlusion Analysis | Highlighted occluded regions with confidence | Toggle |
| Graph Network | Road topology with node/edge rendering | Click for details |
| Centrality Heatmap | Color-coded criticality overlay | Metric selector |
| Resilience Simulation | Animated disruption scenarios | Play, step, reset |
| Alternative Routes | Highlighted backup paths | Route comparison |

---

*Populated after architecture design is complete.*
