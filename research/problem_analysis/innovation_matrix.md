# Innovation Matrix

**Date**: 2026-06-26  
**Project**: ATLAS — Route Resilience (PS-4)  
**Purpose**: To aggressively filter out "cool but impossible" ideas and focus exclusively on high-ROI features for the hackathon.

---

## The Matrix

| Innovation | Problem Solved | Tech Difficulty | Hackathon Feasibility | Judge Impact | Impl. Cost (Hours) | Research Novelty | Deployment Potential | Commercial Potential |
|---|---|---|---|---|---|---|---|---|
| **1. Pre-computed "Hero City" Gamification** | Live demo timeouts ($O(VE)$ centrality) | Low | High | Critical | 5h | Low | Low | High (Demo sales) |
| **2. Interactive Spatial Disasters (Flood Tool)** | Meaningless random node deletion | Medium | High | Critical | 8h | Low | High | High (Insurance/Gov) |
| **3. MST Gap Bridging (Topology Cleaning)** | Mathematically broken graphs | Medium | High | High | 10h | Low | High | High (Mapping APIs) |
| **4. Topology-Aware Loss (clDice)** | High mIoU but visually disconnected roads | High | Medium | High | 15h | Medium | High | Medium (Niche) |
| **5. Confidence-Weighted Routing** | Routing over AI hallucinations | Medium | High | Medium | 8h | Medium | High | High (Logistics) |
| **6. Multi-Modal Fusion (Optical + SAR)** | Complete cloud coverage opacity | Very High | Low | High | 40h+ | High | Critical | Critical (Military/Disaster) |
| **7. Direct-to-Graph Extraction (Sat2Graph)** | Mask-to-vector conversion artifacts | Very High | Low | High | 40h+ | High | High | High (Mapping) |
| **8. Spatiotemporal Cloud Removal (Transformers)** | Hallucinations under large clouds | Extreme | Very Low | High | 60h+ | Extreme | High | Critical (Earth Obs) |
| **9. GNN for Dynamic Bottlenecks** | Real-time centrality computation on $O(VE)$ | Extreme | Very Low | High | 50h+ | High | High | Medium |

---

## Ranking & Recommendations

We rank the innovations by calculating an ROI score: **(Judge Impact / Implementation Cost) × Hackathon Feasibility**.

### 🟢 TIER 1: Approved for Hackathon Implementation (Must-Haves)
*These maximize "Wow Factor" and mathematical correctness while keeping implementation hours low.*

1. **Pre-computed "Hero City" Gamification**
   - **Why**: Zero risk. Guarantees a flawless, instant, 60fps presentation while competitors stare at loading bars.
2. **Interactive Spatial Disasters (Flood Tool)**
   - **Why**: Allows judges to draw a bounding box and watch the city re-route instantly. Visually stunning, high engineering value, simple to implement on the frontend.
3. **MST Gap Bridging (Topology Cleaning)**
   - **Why**: Protects us if the AI model performs poorly. Guarantees a single connected Giant Component, which is mandatory for the routing algorithms to actually work.

### 🟡 TIER 2: Stretch Goals (Implement only if Tier 1 is done early)
*These are valuable but carry training/algorithmic risks.*

4. **Topology-Aware Loss (clDice)**
   - **Why**: Directly addresses the "fragmentation" complaint in the problem statement. However, custom loss functions are notoriously difficult to stabilize during training.
5. **Confidence-Weighted Routing**
   - **Why**: Easy to implement (just pass the softmax output to the graph edge weights), but hard to visualize effectively for the judges.

### 🔴 TIER 3: Rejected for Hackathon (Too Complex)
*These will cause us to fail the hackathon due to time constraints, but should be listed in the "Future Roadmap" slide to show architectural vision.*

6. **Multi-Modal Fusion (Optical + SAR)**
7. **Direct-to-Graph Extraction (Sat2Graph)**
8. **Spatiotemporal Cloud Removal (Transformers)**
9. **GNN for Dynamic Bottlenecks**

---

## Conclusion
The engineering strategy is locked: We will focus heavily on **Tier 1**, ensuring the graph layer is mathematically robust and the frontend is visually spectacular and perfectly responsive. We will fake heavy computation via pre-calculated datasets to guarantee demo success.
