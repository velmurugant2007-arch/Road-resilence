# Future Ideas & Innovation Backlog

## Project ATLAS — Route Resilience
### Bharatiya Antariksh Hackathon 2026 (ISRO) — PS-4

> Captures innovation ideas, future enhancements, and creative solutions that emerge during research and development. Ideas are tagged by domain, feasibility, and judging impact. This is a living document — anyone can add ideas at any time.

---

## Idea Format

```
### IDEA-XXXX: [Title]

- **Domain**: [AI / Graph / GIS / Dashboard / System]
- **Source**: [Research / Brainstorm / Problem Analysis / Video Analysis]
- **Feasibility**: [Hackathon-feasible / Post-hackathon / Research-grade]
- **Judging Impact**: [High / Medium / Low]
- **Description**: [What and why]
- **Implementation Notes**: [How, if known]
- **Status**: Proposed / Accepted / Implemented / Deferred
```

---

## Ideas

### IDEA-0001: Synthetic Occlusion Data Augmentation Pipeline

- **Domain**: AI / Data
- **Source**: Problem Analysis
- **Feasibility**: Hackathon-feasible
- **Judging Impact**: High
- **Description**: Build a pipeline that programmatically generates occluded satellite imagery by overlaying realistic cloud masks, tree canopy patterns, and building shadows onto clean road imagery. This would demonstrate understanding of the occlusion problem and provide unlimited training data for occlusion scenarios.
- **Implementation Notes**: Use Perlin noise for cloud generation, vegetation masks from spectral indices, shadow simulation from building footprints and sun angle.
- **Status**: Proposed

### IDEA-0002: Network Resilience Simulation Under Disruption

- **Domain**: Graph
- **Source**: Problem Title Analysis
- **Feasibility**: Hackathon-feasible
- **Judging Impact**: High
- **Description**: Simulate cascading failure scenarios on the road network — what happens when critical nodes are removed? Visualize the impact on connectivity, travel times, and alternative routes. This directly addresses "criticality analysis" in the problem title.
- **Implementation Notes**: Sequential node removal by centrality rank, measure network diameter and component count at each step, animate in dashboard.
- **Status**: Proposed

### IDEA-0003: Confidence-Weighted Graph Construction

- **Domain**: AI + Graph
- **Source**: Brainstorm
- **Feasibility**: Hackathon-feasible
- **Judging Impact**: High
- **Description**: Instead of binary road/non-road segmentation feeding into graph construction, use the model's prediction confidence to weight graph edges. Low-confidence roads (likely occluded or uncertain) get lower weights, affecting criticality analysis naturally.
- **Implementation Notes**: Use softmax probabilities from segmentation model as edge confidence; integrate into graph edge attributes.
- **Status**: Proposed

---

*Ideas are continuously captured. Evaluation happens during architecture and implementation phases.*
