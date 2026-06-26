# Graph Theory & Network Science

## Project ATLAS — Route Resilience
### Knowledge Base Entry

> This page documents all graph theory knowledge applied to road network analysis — construction algorithms, centrality metrics, resilience measures, and the mathematical foundations behind each approach.

---

## Problem Context

The Graph module transforms extracted road segments into a topological network and performs **criticality analysis** — identifying nodes and edges whose failure would most severely impact urban mobility.

---

## Pipeline Overview

```
Road Segmentation Mask
        ↓
   Skeletonization (thinning to 1-pixel width)
        ↓
   Graph Construction (nodes at intersections, edges as road segments)
        ↓
   Topology Healing (connect broken segments, remove artifacts)
        ↓
   Attribute Assignment (edge lengths, road widths, confidence scores)
        ↓
   Centrality Analysis (identify critical infrastructure)
        ↓
   Resilience Simulation (cascading failure analysis)
        ↓
   Alternative Route Analysis (redundancy assessment)
```

---

## Key Algorithms

### Skeletonization
**Purpose**: Reduce binary road mask to 1-pixel-wide skeleton preserving topology.
- Zhang-Suen thinning algorithm
- Morphological skeletonization
- Medial axis transform
- **Selection**: Deferred to Phase 5 (Architecture)

### Graph Construction
**Purpose**: Convert skeleton pixels into a graph where intersections are nodes and road segments are edges.
- Pixel connectivity analysis (8-connected neighborhood)
- Junction detection (pixels with >2 neighbors)
- Edge tracing between junctions
- Coordinate assignment (pixel → geographic)

### Topology Healing
**Purpose**: Repair disconnections caused by imperfect segmentation or occlusion.
- Gap bridging (connect endpoints within threshold distance)
- Spur removal (remove dangling edges below minimum length)
- Loop simplification
- Minimum Spanning Tree (MST) for component connection
- Steiner tree approximation for optimal reconnection

### Centrality Metrics
**Purpose**: Identify critical nodes and edges in the network.

| Metric | What It Measures | Why It Matters |
|---|---|---|
| **Betweenness Centrality** | Fraction of shortest paths passing through a node/edge | Identifies bottlenecks — removal causes maximum rerouting |
| **Closeness Centrality** | Inverse sum of shortest distances to all other nodes | Identifies most accessible locations |
| **Eigenvector Centrality** | Influence based on connections to other influential nodes | Identifies systemically important nodes |
| **Degree Centrality** | Number of connections | Identifies major intersections |
| **Bridge Detection** | Edges whose removal disconnects the graph | Identifies single points of failure |

### Resilience Analysis
**Purpose**: Quantify network robustness under disruption scenarios.

- **Sequential node removal** — Remove nodes by centrality rank, measure connectivity
- **Random failure simulation** — Random node/edge removal, measure degradation
- **Targeted attack simulation** — Remove highest-centrality nodes first
- **Resilience Index** — Ratio of network performance before/after disruption
- **Percolation threshold** — Fraction of nodes removable before network fragments

### Alternative Route Analysis
**Purpose**: Assess redundancy and identify areas with no alternative paths.
- K-shortest paths between critical node pairs
- Disjoint path analysis (edge-disjoint, node-disjoint)
- Travel time comparison (primary vs. alternative routes)

---

## Mathematical Foundations

### Betweenness Centrality

$$C_B(v) = \sum_{s \neq v \neq t} \frac{\sigma_{st}(v)}{\sigma_{st}}$$

Where σ_st is the total number of shortest paths from s to t, and σ_st(v) is the number passing through v.

### Closeness Centrality

$$C_C(v) = \frac{n - 1}{\sum_{u \neq v} d(v, u)}$$

Where d(v,u) is the shortest-path distance between v and u.

### Resilience Index

$$R = \frac{\text{Performance after disruption}}{\text{Performance before disruption}}$$

Performance can be measured as: largest connected component size, average shortest path length, network diameter, or total reachability.

---

## Libraries to Evaluate

| Library | Language | Strengths | Considerations |
|---|---|---|---|
| NetworkX | Python | Rich algorithms, easy API | Slow for large graphs |
| graph-tool | Python/C++ | Very fast, statistical | Complex installation |
| igraph | Python/C | Fast, good centrality | Less intuitive API |
| OSMnx | Python | Road network specific | Depends on OpenStreetMap |

---

*This page is updated after every graph-related research finding and implementation decision.*
