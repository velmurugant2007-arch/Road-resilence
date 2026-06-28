# Software Requirements Specification (SRS)

**Project**: ATLAS — Route Resilience (Bharatiya Antariksh Hackathon 2026 - PS-4)
**Version**: 1.0
**Status**: APPROVED

---

## 1. Introduction
This document is the definitive specification for the Route Resilience project. It captures all functional, non-functional, and hidden requirements extracted from the official ISRO problem statement, guiding the architecture, development, and testing phases.

## 2. Functional Requirements (FR)
| ID | Requirement | Evaluation Mapping | Input | Output |
|---|---|---|---|---|
| **FR-01** | The system shall accept high-resolution optical satellite imagery (GeoTIFF, PNG). | Input Validation | GeoTIFF/PNG file | Standardized Image Tensor |
| **FR-02** | The system shall perform semantic segmentation to extract road networks, maintaining connectivity under occlusions (clouds/shadows). | Connectivity (IoU on Graph) | Image Tensor | Binary Probability Mask |
| **FR-03** | The system shall reconstruct and output a visually represented confidence map indicating occlusion severity and model certainty. | Real-World Utility | Probability Mask | Heatmap Overlay |
| **FR-04** | The system shall convert the semantic road mask into a topologically continuous Graph structure. | Graph Accuracy | Binary Mask | NetworkX Graph |
| **FR-05** | The system shall automatically bridge false disconnections (gaps) caused by model failure or occlusions up to a configurable distance threshold. | Breaks / km | NetworkX Graph | Healed NetworkX Graph |
| **FR-06** | The system shall compute Betweenness Centrality (BC), CFFBC, a-Centrality, and k-Core for every node/edge in the graph. | Mathematical Correctness | Healed Graph | Graph + Centrality Metrics |
| **FR-07** | The system shall allow users to define a spatial bounding box to simulate a disaster (e.g., flood) that disables infrastructure within the region. | Resilience Simulation | Bounding Box Coords | Degraded Sub-Graph |
| **FR-08** | The system shall calculate a Resilience Score by comparing the Giant Component Size before and after a simulated disaster. | Network Connectivity | Original Graph, Degraded Graph | Delta Resilience Score |
| **FR-09** | The system shall visualize the road network, centrality heatmaps, and simulated disruptions on an interactive web dashboard. | Presentation Quality | JSON Graph Data | UI Render |

## 3. Non-Functional Requirements (NFR)
| ID | Requirement | Evaluation Mapping | Constraint |
|---|---|---|---|
| **NFR-01** | The system shall pre-compute heavy $O(VE)$ centrality metrics for the "Hero City" to ensure zero-latency interactive simulations during the demo. | Engineering Excellence | API response < 200ms |
| **NFR-02** | The system components (AI, Graph, GIS, Backend, Frontend) shall be strictly decoupled to allow independent scaling and testing. | Scalability | Microservice-ready APIs |
| **NFR-03** | The UI shall provide a fluid, 60fps interaction experience when switching between satellite view and centrality heatmaps. | User Experience | WebGL/Canvas rendering |
| **NFR-04** | The codebase shall conform to PEP8 standards with full type hinting and docstrings. | Maintainability | Strict linting enforcement |

## 4. Hidden Requirements (Extracted via Analysis)
| ID | Hidden Requirement | Justification | Impact |
|---|---|---|---|
| **HR-01** | **Topological Priority over mIoU** | The problem explicitly complains about "fragmentation". A model with 90% mIoU but 50 broken segments fails the core objective compared to an 85% mIoU model with 0 broken segments. | Requires topological loss functions (clDice). |
| **HR-02** | **Algorithmic Graph Healing** | Even the best AI cannot perfectly guess road structures under 100% opaque clouds. The pipeline *must* have a post-processing heuristic to force mathematical continuity. | Requires MST or A* gap bridging logic. |
| **HR-03** | **Spatially Correlated Failures** | Real disasters don't delete nodes randomly. They destroy contiguous geographic zones. | The dashboard must use bounding boxes, not random node dropout. |

## 5. Constraints and Assumptions
### Constraints
- **Hardware**: The solution must be capable of live demonstration on standard hackathon laptops (forcing the pre-computation strategy).
- **Data Availability**: The system is constrained to open-source Optical imagery; SAR fusion is deferred due to time limitations.

### Assumptions
- **Optical Sufficiency**: We assume that topological loss + geometric priors + MST heuristics can sufficiently mitigate the lack of SAR cloud-penetration data.
- **Pre-Computation Acceptance**: We assume judges will evaluate the mathematical correctness of the interactive disruption rather than demanding a live graph extraction of a newly uploaded 10GB GeoTIFF.

## 6. Requirement Traceability Matrix (RTM) Summary
*Every architecture component traces directly back to this SRS. The Testing Strategy will validate every FR and NFR listed above.*
