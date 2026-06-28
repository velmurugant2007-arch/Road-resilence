# Mathematical Design Document

**Project**: ATLAS — Route Resilience
**Status**: APPROVED (Post-CER Revisions)

> **Purpose**: This document specifies the mathematical formulations governing the AI extraction, topological healing, graph centrality computations, and resilience scoring.

---

## 1. Image Segmentation Mathematics (Topology-Aware)
Standard cross-entropy loss ($\mathcal{L}_{CE}$) penalizes pixel mismatches equally, which fails to preserve thin road topologies. 
We utilize **clDice (centerline-Dice) Loss**. 

**Differentiability Patch (Soft-Skeletonization)**: Standard skeletonization algorithms (like Zhang-Suen) are non-differentiable. To use clDice inside a PyTorch training loop, we approximate the skeleton $S_P$ using iterative min-pooling and max-pooling operations over the probability mask $P$.

$$ T_{prec} (Precision) = \frac{|S_P \cap L|}{|S_P|} $$
$$ T_{sens} (Sensitivity) = \frac{|S_L \cap P|}{|S_L|} $$

The clDice metric is the harmonic mean:
$$ clDice = 2 \times \frac{T_{prec} \times T_{sens}}{T_{prec} + T_{sens}} $$
$$ \mathcal{L}_{total} = \alpha \mathcal{L}_{Dice} + (1 - \alpha)(1 - clDice) $$

## 2. Skeletonization and Vectorization (Inference)
During inference, the binary probability mask is converted to a 1-pixel wide skeleton using the discrete **Zhang-Suen thinning algorithm**. Nodes ($V$) are placed at intersections and endpoints. Edges ($E$) are pixel paths.

**CRS Reprojection**: Before assigning physical edge weights (meters), nodes are reprojected from image pixel space $\rightarrow$ geographic `EPSG:4326` $\rightarrow$ local projected UTM (e.g., `EPSG:32643`). This ensures Euclidean distance math is physically valid.

## 3. Graph Healing (Hybrid Cost Function)
To fix fragments, we do not rely on purely Euclidean Minimum Spanning Trees (which blindly cut through buildings). We implement a **Hybrid Cost Function** to evaluate potential bridging edges between degree-1 nodes.

For any candidate edge $e_{uv}$, the traversal cost $C_{uv}$ is a weighted sum:
$$ C_{uv} = w_1 \cdot D(u,v) + w_2 \cdot (1 - P(e_{uv})) + w_3 \cdot \theta(u,v) + w_4 \cdot W(u,v) + w_5 \cdot \rho(u,v) $$

Where:
- $D(u,v)$: **Euclidean Distance** (meters).
- $P(e_{uv})$: **AI Confidence Integral** (Average Softmax probability along the line segment between $u$ and $v$).
- $\theta(u,v)$: **Directional Consistency** (Angular penalty if connecting the nodes requires a sharp hairpin turn from their existing vector).
- $W(u,v)$: **Road Width Prior** (Penalty for connecting a massive 6-lane highway to a 1-lane alley).
- $\rho(u,v)$: **Local Road Density** (Penalty for creating new roads in areas known to be empty fields).

Edges with the lowest $C_{uv}$ are added iteratively until the maximum sensible distance threshold is reached.

## 4. Graph Theory & Centrality Analysis
For a connected component within $G_{healed}$:
- **Betweenness Centrality (BC)**: Proportion of shortest paths passing through a node. Identifies bottlenecks.
- **Closeness Centrality (CC)**: Inverse sum of shortest distances to all other nodes.
- **K-Core Decomposition**: Maximal subgraph where all vertices have degree $\ge k$. Identifies core urban density.

## 5. Stress Simulation & Resilience Scoring
A disaster (bounding box $B$) drops intersecting edges.
$$ Resilience Score = \frac{|V(GC_{degraded})|}{|V(GC_{original})|} $$
A resilient network maintains a score close to 1.0 even under stress.
