# Deliverable 6: ATLAS Dashboard Page Wireframes

This document provides ASCII spatial layout wireframes for all 8 operational views of the ATLAS platform. In all views, the underlying WebGL Mapbox canvas fills 100% of the screen background.

---

## 1. Overview Page (Mission Control)
Focuses on baseline Hero City telemetry, global network health, and high-level structural metrics.

```text
+-----------------------------------------------------------------------------------+
| [ATLAS Logo]  HERO CITY: BENGALURU | STATUS: HEALTHY (42ms) | [Docs] [GitHub] [OS] |
+-----------------------------------------------------------------------------------+
| [N] |                                                      | +------------------+ |
| [O] |                                                      | | TOTAL NODES      | |
| [V] |                  WEBGL MAP CANVAS                    | | 176              | |
| [E] |             (CartoDB Dark Matter Base)               | +------------------+ |
| [R] |                                                      | +------------------+ |
| [V] |         [Cyan Baseline Road Polylines]               | | TOTAL EDGES      | |
| [I] |                                                      | | 212              | |
| [E] |                                                      | +------------------+ |
| [W] |                                                      | +------------------+ |
|     |                                                      | | EFFICIENCY SCORE | |
|     |                                                      | | 0.842            | |
|     |                                                      | +------------------+ |
+-----------------------------------------------------------------------------------+
```

---

## 2. AI Road Extraction Page
Allows toggling synthetic cloud occlusions and observing SegFormer probability heatmaps.

```text
+-----------------------------------------------------------------------------------+
| [ATLAS] VIEW: AI ROAD EXTRACTION                              | [Threshold: 0.65] |
+-----------------------------------------------------------------------------------+
| [A] |                                                      | +------------------+ |
| [I] |          [Purple AI Probability Heatmap]             | | OCCLUSION FILTER | |
|     |                                                      | | (*) Cloud Mask   | |
| [E] |           ~~~ Synthetic Cloud Overlay ~~~            | | ( ) Shadow Mask  | |
| [X] |                                                      | +------------------+ |
| [T] |                                                      | +------------------+ |
| [R] |                                                      | | AI METRICS       | |
| [A] |                                                      | | clDice: 0.842    | |
| [C] |                                                      | | IoU:    0.781    | |
| [T] |                                                      | +------------------+ |
+-----------------------------------------------------------------------------------+
```

---

## 3. Graph Construction Page
Displays skeletonized polylines vs simplified RDP edges.

```text
+-----------------------------------------------------------------------------------+
| [ATLAS] VIEW: GRAPH CONSTRUCTION & VECTORIZATION              | [RDP Eps: 2.0m]   |
+-----------------------------------------------------------------------------------+
| [G] |                                                      | +------------------+ |
| [R] |         [Green Node Junction Markers]                | | VECTOR CONTROLS  | |
| [A] |                       O                              | | RDP Tolerance    | |
| [P] |                      / \                             | | [====|=======] 2m| |
| [H] |                     O---O                            | | Spur Pruning     | |
|     |                                                      | | [==|=========] 15| |
| [C] |                                                      | +------------------+ |
| [O] |                                                      | +------------------+ |
| [N] |                                                      | | COMPONENTS: 1    | |
| [S] |                                                      | | AVG DEGREE: 2.4  | |
+-----------------------------------------------------------------------------------+
```

---

## 4. Graph Healing Page (XAI Explainability Focus)
Highlights re-connected road gaps and pops up the XAI inspector panel upon edge click.

```text
+-----------------------------------------------------------------------------------+
| [ATLAS] VIEW: GRAPH HEALING XAI INSPECTOR                     | [Search Rad: 150m]|
+-----------------------------------------------------------------------------------+
| [G] |                                                      | +------------------+ |
| [R] |       O======= [Pulsating Healed Edge] =======O      | | XAI EXPLANATION  | |
| [A] |       |            (Click to inspect)         |      | | ID: RH-001 [ACC] | |
| [P] |                                                      | | Dist Score: 0.92 | |
| [H] |                                                      | | AI Conf:    0.91 | |
|     |                                                      | | Dir Score:  0.96 | |
| [H] |                                                      | | Hybrid:     0.93 | |
| [E] |                                                      | |------------------| |
| [A] |                                                      | | "Accepted due to | |
| [L] |                                                      | | strong alignment"| |
+-----------------------------------------------------------------------------------+
```

---

## 5. Criticality Analysis Page
Colors road segments from green (low risk) to neon magenta/red (critical bottleneck).

```text
+-----------------------------------------------------------------------------------+
| [ATLAS] VIEW: GRAPH CRITICALITY & VULNERABILITY               | [Metric: Between] |
+-----------------------------------------------------------------------------------+
| [C] |                                                      | +------------------+ |
| [R] |         \                                            | | CRITICALITY MENU | |
| [I] |          \ [Neon Magenta Bottleneck Link]            | | (*) Betweenness  | |
| [T] |           O===================O                      | | ( ) Closeness    | |
| [I] |                                \                     | | ( ) K-Core Shell | |
| [C] |                                 \ [Green Link]       | +------------------+ |
| [A] |                                                      | +------------------+ |
| [L] |                                                      | | BRIDGES DETECTED | |
|     |                                                      | | 4 Cut-Vertices   | |
+-----------------------------------------------------------------------------------+
```

---

## 6. Stress Simulation Page & 7. Decision Support Page
Combined workflow: user defines disaster blast zone, triggers disaster, and reviews ranked emergency repairs.

```text
+-----------------------------------------------------------------------------------+
| [ATLAS] VIEW: STRESS SIMULATION & DECISION SUPPORT            | [Fraction: 15%]   |
+-----------------------------------------------------------------------------------+
| [S] |                                                      | +------------------+ |
| [I] |            ((( [Red Disaster Blast Zone] )))         | | DECISION SUPPORT | |
| [M] |                     X     X                          | | EMERGENCY RANK   | |
|     |                   (Severed Links)                    | | #1 Link E-104    | |
| [D] |                                                      | |    Delta R: +4.2%| |
| [E] |                                                      | | #2 Link E-088    | |
| [C] |                                                      | |    Delta R: +3.1%| |
| [I] |                                                      | | [HIGHLIGHT ROUTE]| |
| [S] |+----------------------------------------------------+| +------------------+ |
| [I] || [|<] [Play] [>|] Failure Step Timeline Scrubbing   ||                      |
+-----------------------------------------------------------------------------------+
```

---

## 8. System Configuration Page
Allows fine-tuning API parameters, weights, and server connections.

```text
+-----------------------------------------------------------------------------------+
| [ATLAS] VIEW: SYSTEM CONFIGURATION & THRESHOLDS                                   |
+-----------------------------------------------------------------------------------+
| [C] |  +-----------------------------------------------------------------------+  |
| [O] |  | GLOBAL COMPOSITE CRITICALITY WEIGHTS                                  |  |
| [N] |  | Betweenness Centrality Weight: [====|======] 0.30                       |  |
| [F] |  | Closeness Centrality Weight:   [===|=======] 0.20                       |  |
| [I] |  | K-Core Shell Decomposition:    [==|========] 0.10                       |  |
| [G] |  |                                                                       |  |
|     |  | AI & HEALING THRESHOLDS                                               |  |
|     |  | Min Barrier Veto Confidence:   [===|=======] 0.30                       |  |
|     |  |                                            [RESET DEFAULTS] [SAVE]    |  |
|     |  +-----------------------------------------------------------------------+  |
+-----------------------------------------------------------------------------------+
```
