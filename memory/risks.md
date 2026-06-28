# Risk Register & Heat Map

## Project ATLAS — Route Resilience
### Bharatiya Antariksh Hackathon 2026 (ISRO) — PS-4

> **Purpose**: This living document categorizes all project risks, mapping their Probability against their Impact to form a Risk Heat Map. It ensures that mitigation strategies are actively integrated into our architecture.

---

## 🌡️ Risk Heat Map Summary

| Probability \ Impact | Low Impact | Medium Impact | High Impact | Critical Impact |
|---|---|---|---|---|
| **High Probability** | | Timeline (T-01) | Dataset (D-01) | Performance (P-01) |
| **Medium Probability** | | | AI (A-01), Judge (J-01) | Presentation (PR-01) |
| **Low Probability** | Deployment (DP-01) | | Technical (TC-01) | AI (A-02) |

---

## 1. Technical Risks

| ID | Risk Description | Probability | Impact | Mitigation |
|---|---|---|---|---|
| **TC-01** | **Graph Disconnection**<br>Topological cleaning heuristics (MST) bridge gaps across impossible physical barriers (e.g., rivers). | 🟢 Low | 🔴 High | Hardcode conservative maximum distance thresholds (e.g., <30m) and penalize gap-bridging over known water bodies if OSM data is available. |

## 2. AI Risks

| ID | Risk Description | Probability | Impact | Mitigation |
|---|---|---|---|---|
| **A-01** | **Topological Training Instability**<br>Custom loss functions like clDice cause the model to diverge during training. | 🟡 Med | 🔴 High | Start with standard Cross-Entropy/Dice to establish a baseline, then fine-tune with clDice at a very low learning rate. |
| **A-02** | **Hallucination under Occlusion**<br>Model invents non-existent roads under massive continuous cloud cover based purely on geometric priors. | 🟢 Low | 🔴 Critical | Expose softmax confidence to the graph. Visually mark hallucinated edges as "Low Confidence" in the dashboard. |

## 3. Dataset Risks

| ID | Risk Description | Probability | Impact | Mitigation |
|---|---|---|---|---|
| **D-01** | **Scarcity of Occluded Indian Data**<br>Lack of high-quality, open-source Indian urban datasets featuring ground-truth roads *with* cloud/shadow occlusions. | 🔴 High | 🔴 High | Use synthetic data augmentation: programmatically overlay cloud masks and shadow polygons onto clear satellite imagery (e.g., SpaceNet) during training. |

## 4. Performance Risks

| ID | Risk Description | Probability | Impact | Mitigation |
|---|---|---|---|---|
| **P-01** | **Centrality Computation Bottleneck**<br>Calculating exact Betweenness Centrality on a city-scale graph ($O(VE)$) freezes the API. | 🔴 High | 🔴 Critical | Do not compute BC live. Pre-compute centrality for the "Hero City" offline. For live disruption simulations, use fast approximations or localized sub-graphs. |

## 5. Presentation Risks

| ID | Risk Description | Probability | Impact | Mitigation |
|---|---|---|---|---|
| **PR-01** | **Live Demo Crash**<br>The system times out or throws an unhandled exception while a judge is interacting with it. | 🟡 Med | 🔴 Critical | The "Hero City" MVP strategy. All heavy ML/Graph processing is done offline; the dashboard only queries pre-computed static JSONs and runs lightweight routing logic. |

## 6. Timeline Risks

| ID | Risk Description | Probability | Impact | Mitigation |
|---|---|---|---|---|
| **T-01** | **AI Rabbit Hole**<br>The team spends 70% of the hackathon tuning the AI model, leaving no time to build the Graph Analysis or Dashboard. | 🔴 High | 🟡 Med | Timebox AI training. If the model isn't perfect by hour 12, freeze the weights, accept the fragmented output, and rely on the Graph Module's Topological Cleaning to fix it. |

## 7. Deployment Risks

| ID | Risk Description | Probability | Impact | Mitigation |
|---|---|---|---|---|
| **DP-01** | **Submission Size Exceeded**<br>Docker images with PyTorch and GIS libraries exceed the hackathon portal's upload limit. | 🟢 Low | 🟢 Low | Use multi-stage Docker builds. Use `pytorch-cpu` for the deployment container if inference speed is not strictly timed, drastically reducing image size. |

## 8. Judge Risks

| ID | Risk Description | Probability | Impact | Mitigation |
|---|---|---|---|---|
| **J-01** | **Missed Engineering Value**<br>Judges perceive the solution as just another semantic segmentation project and ignore the complex graph mathematics behind it. | 🟡 Med | 🔴 High | Build the UI to explicitly highlight the mathematics. Include a side-by-side "Pixel vs Topology" slider and live charts showing Giant Component Size degradation. |

---

*This document is reviewed continuously. Risks are mitigated through architectural decisions documented in ADRs.*
