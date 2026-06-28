# Research Notebook

## Project ATLAS — Route Resilience
### Bharatiya Antariksh Hackathon 2026 (ISRO) — PS-4

---

**Purpose**: Chronological log of all research activities, findings, and their implications for the project. Every research entry includes the question investigated, methodology, findings, and engineering impact.

---

## Entry Format

```
### RN-XXXX: [Research Title]

**Date**: YYYY-MM-DD
**Researcher**: [Team/Role]
**Domain**: [AI / Graph / GIS / Data / General]
**Question**: What specific question does this research address?

**Methodology**:
- How was the research conducted?

**Findings**:
- What was discovered?

**Engineering Impact**:
- How does this affect the project design or implementation?

**References**:
- Papers, links, datasets consulted

**Status**: Complete / In Progress / Superseded
```

---

## Entries

### RN-0001: Problem Statement Deconstruction

**Date**: 2026-06-26
**Researcher**: AI/ML Engineer & Graph Theory Engineer
**Domain**: General / System
**Question**: What are the true technical requirements of PS-4, beyond the text description?

**Methodology**:
- Sentence-by-sentence textual analysis of the official ISRO PS-4 description.
- Visual inspection and reverse-engineering of the provided architecture and results diagrams.

**Findings**:
- The problem is not just semantic segmentation; it is **topology-preserving semantic segmentation**. Standard metrics like mIoU are insufficient.
- The diagram explicitly names required evaluation metrics: `Connectivity (IoU on Graph)` and `Breaks / km`.
- The diagram explicitly lists centrality metrics to implement: `Betweenness Centrality (BC)`, `CFFBC`, `a-Centrality`, and `k-Core`.
- Resilience must be measured by tracking `Network Connectivity (Giant Component Size)` against disruption scenarios.
- The pipeline explicitly requires a "Topological Cleaning" step after graph construction.

**Engineering Impact**:
- Forces a shift in the AI module: loss functions must incorporate topological priors (e.g., clDice).
- Forces the Graph module to implement sophisticated gap-bridging algorithms to achieve the required "mathematically continuous" state.
- Clearly defines the exact metrics the QA module must implement for evaluation.

**References**:
- `research/problem_analysis/ps4_analysis.md`
- Problem Statement text and diagrams provided by user.

**Status**: Complete

---

### RN-0002: Competitive Intelligence & Strategy

**Date**: 2026-06-26
**Researcher**: Senior Software Architect & Hackathon Judge
**Domain**: Strategy / Architecture
**Question**: How will competing teams approach PS-4, and where are their architectural blind spots?

**Methodology**:
- Adversarial thinking and hackathon meta-analysis.

**Findings**:
- 90% of teams will fall into the "mIoU Trap", building basic Semantic Segmentation models (UNet) that yield high pixel accuracy but topologically broken masks.
- Teams will suffer from live demonstration timeouts because computing exact Betweenness Centrality on large graphs is $O(VE)$.
- Most teams will connect the AI directly to Graph extraction without the critical "Topological Cleaning" phase, resulting in mathematically useless graphs.

**Engineering Impact (Our Differentiators)**:
1. **Pre-computed Hero City**: We will bypass live-compute latency during the demo by pre-computing a massive graph of Bengaluru, allowing instantaneous interactive simulation.
2. **Spatially-Correlated Disasters**: We will simulate localized failures (e.g., bounding-box floods) rather than mathematically naive random node deletion.
3. **clDice Loss**: We will integrate topology-aware loss functions to guarantee connectivity at the AI layer.
4. **MST Gap Bridging**: We will implement algorithmic gap bridging at the Graph layer to ensure a mathematically continuous giant component.

**References**:
- `research/problem_analysis/competition_strategy_report.md`

**Status**: Complete

---

### RN-0003: Innovation Matrix & Feature Triage

**Date**: 2026-06-26
**Researcher**: Senior Software Architect
**Domain**: Strategy / Prioritization
**Question**: Which innovations provide the highest judging ROI without risking hackathon failure?

**Methodology**:
- Matrix analysis evaluating Problem Solved, Tech Difficulty, Hackathon Feasibility, Judge Impact, Implementation Cost, Research Novelty, Deployment Potential, and Commercial Potential.

**Findings**:
- Complex AI solutions (SAR fusion, Spatiotemporal Transformers, GNNs) have 40-60+ hour implementation costs and are highly unstable. They will cause hackathon failure.
- UX and Algorithmic heuristics (MST Gap Bridging, Pre-computed dashboards, Bounding-box disaster simulation) have 5-10 hour implementation costs and massive visual/judging impact.

**Engineering Impact**:
- **Approved (Tier 1)**: Pre-computed "Hero City", Interactive Spatial Disasters, MST Gap Bridging.
- **Stretch (Tier 2)**: clDice Topology Loss, Confidence-Weighted Routing.
- **Rejected (Tier 3)**: SAR Fusion, Sat2Graph, Spatiotemporal models, GNNs. (Will be placed on the Future Roadmap slide).

**References**:
- `research/problem_analysis/innovation_matrix.md`

**Status**: Complete

---

*New entries are appended chronologically. Older entries are never deleted — they form the research provenance trail.*
