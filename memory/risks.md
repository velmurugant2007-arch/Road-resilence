# Risk Register

## Project ATLAS — Route Resilience
### Bharatiya Antariksh Hackathon 2026 (ISRO) — PS-4

> Active risk tracking with severity assessment, likelihood, and mitigation strategies. Reviewed and updated at each phase transition.

---

## Risk Matrix

| Severity ↓ / Likelihood → | Low | Medium | High |
|---|---|---|---|
| **Critical** | Monitor | Mitigate Actively | Immediate Action |
| **High** | Monitor | Mitigate | Mitigate Actively |
| **Medium** | Accept | Monitor | Mitigate |
| **Low** | Accept | Accept | Monitor |

---

## Active Risks

### RISK-001: Insufficient training data for occlusion scenarios

- **Severity**: Critical
- **Likelihood**: Medium
- **Category**: Data
- **Phase Identified**: Phase 1
- **Status**: Open
- **Description**: Road extraction under heavy occlusion (cloud cover, dense vegetation, building shadows) may require specialized training data that is not readily available in standard satellite imagery datasets.
- **Impact**: Model cannot generalize to occluded road segments, reducing extraction accuracy and graph completeness.
- **Mitigation**:
  1. Survey multiple datasets (SpaceNet, DeepGlobe, INRIA, Massachusetts Roads) for occlusion presence
  2. Design data augmentation pipeline to simulate occlusion (cloud overlay, shadow injection)
  3. Investigate self-supervised or semi-supervised approaches that require less labeled data
- **Owner**: AI/ML Engineer
- **Review Date**: Phase 2

### RISK-002: Graph disconnection from imperfect road extraction

- **Severity**: High
- **Likelihood**: High
- **Category**: Algorithm
- **Phase Identified**: Phase 1
- **Status**: Open
- **Description**: If the AI model misses road segments (especially under occlusion), the resulting road network graph will have disconnected components, rendering topology analysis unreliable.
- **Impact**: Criticality metrics (betweenness, closeness centrality) become meaningless on disconnected graphs.
- **Mitigation**:
  1. Design topology healing algorithms in the graph module
  2. Implement skeletonization post-processing to connect near-miss segments
  3. Use minimum spanning tree or Steiner tree approaches for gap bridging
- **Owner**: Graph Theory Engineer
- **Review Date**: Phase 5

### RISK-003: Time pressure compromising engineering quality

- **Severity**: High
- **Likelihood**: Medium
- **Category**: Process
- **Phase Identified**: Phase 1
- **Status**: Open
- **Description**: Hackathon time constraints may pressure the team to skip documentation, testing, or research phases.
- **Impact**: Violates Project Constitution. Reduces final presentation quality. Creates technical debt.
- **Mitigation**:
  1. Phase-gated approach — no phase skipping
  2. Documentation-code parity enforced through templates and checklists
  3. Prioritize features by judging impact, not implementation ease
- **Owner**: Product Manager
- **Review Date**: Each phase transition

### RISK-004: Model inference speed insufficient for real-time dashboard demo

- **Severity**: Medium
- **Likelihood**: Medium
- **Category**: Performance
- **Phase Identified**: Phase 1
- **Status**: Open
- **Description**: Complex segmentation models (e.g., Mask2Former, Swin Transformer) may be too slow for real-time inference during the demonstration.
- **Impact**: Dashboard cannot show live processing; must rely on pre-computed results.
- **Mitigation**:
  1. Select model architecture with inference speed as a key criterion
  2. Implement ONNX runtime or TensorRT optimization
  3. Design dashboard to gracefully handle both live and pre-computed modes
- **Owner**: AI/ML Engineer + Frontend Engineer
- **Review Date**: Phase 8

---

## Closed Risks

*No risks closed yet.*

---

*This register is reviewed at every phase transition and after every significant technical decision.*
