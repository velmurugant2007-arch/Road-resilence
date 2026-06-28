# Competition Strategy & Intelligence Report

**Date**: 2026-06-26  
**Event**: Bharatiya Antariksh Hackathon 2026 (ISRO)  
**Problem Statement**: PS-4 (Route Resilience)  
**Classification**: Internal Strategy  

---

## 1. What will 90% of teams probably build?
The vast majority of teams will build a superficial, sequential pipeline:
- A standard semantic segmentation model trained on open-source data (e.g., SpaceNet or DeepGlobe).
- A basic `cv2.ximgproc.thinning()` skeletonization script to convert the pixel mask into lines.
- A naive `NetworkX` script to compute centrality on those raw, unconnected lines.
- A basic Streamlit or Flask web interface where the user uploads an image and waits 60 seconds to see a static overlaid mask.

## 2. What common AI models will they use?
- **U-Net** (with ResNet34/50 backbones) will be the overwhelming favorite.
- **DeepLabV3+** and **YOLOv8-Seg**. 
- *Crucial Miss*: 95% of teams will use standard Cross-Entropy or Dice Loss, which optimizes for pixel accuracy (mIoU) but completely fails at preserving thin topological connections (roads).

## 3. What architecture will they probably follow?
A **Synchronous Monolith**. They will tie the AI inference, graph construction, and visualization into a single blocking HTTP request. When the judge clicks "Analyze", the entire system will freeze while the GPU computes the mask and the CPU churns through the graph math.

## 4. What fatal mistakes will they make?
- **The mIoU Trap**: They will optimize their model for high mIoU, resulting in thick, highly-scored roads that are disconnected by small 2-pixel gaps under trees. Their graphs will be severely fragmented.
- **Skipping Topological Cleaning**: They will convert the AI output directly to a graph without a gap-bridging heuristic. As a result, their graph analysis will be mathematically meaningless (you can't route across a broken graph).
- **The $O(VE)$ Centrality Timeout**: They will attempt to compute exact Betweenness Centrality on a dense 10,000-node graph *live* during the demonstration. The system will time out or crash in front of the judges.
- **Ignoring the Core Problem**: They will build a "road extractor" rather than an "occlusion-robust resilience analyzer," ignoring the explicit ISRO requirement regarding clouds and shadows.

## 5. Which features are unnecessary?
- **Massive File Uploads**: Building infrastructure to handle 5GB GeoTIFF uploads live is a waste of time.
- **User Authentication**: Login screens add zero engineering value to the PS-4 solution.
- **Training from Scratch**: Wasting 20 hours of the hackathon training a custom architecture from random weights, rather than fine-tuning pre-trained models.

## 6. Which features will impress but provide little engineering value?
- **3D City Rendering**: Extruding buildings using Mapbox GL to look like a modern video game. It looks incredible but contributes absolutely nothing to graph-theoretic criticality or occlusion robustness.
- **"Chat with the Map" LLM Integrations**: Adding an LLM to ask "What is the longest road?" is flashy but distracts from the core graph resilience mathematics required by ISRO.

## 7. Which features genuinely increase judging score?
- **Explainability Visualizations**: A side-by-side slider showing "Standard AI (Broken)" vs. "Our Topology-Aware Pipeline (Connected)" under a cloud occlusion.
- **Mathematical Traceability**: Displaying the exact formulas and metrics used (e.g., showing the Jaccard Overlap of BC vs. k-Core dynamically on screen).
- **Interactive Resilience Demo**: A dashboard where a judge can literally click a road to "block" it, and the system instantly re-routes and updates the Giant Component Size chart in real-time.

## 8. Realistic Differentiators (High Impact, Low Complexity)
How we win without over-engineering:

1. **The "Hero City" Architecture (MVP)**: Instead of a slow live-processing pipeline, we pre-compute the entire pipeline for a massive, dense section of Bengaluru. During the 5-minute pitch, our dashboard is instantly responsive, zero-latency, and interactive, while other teams stare at loading spinners.
2. **Topological Gap Bridging (Post-Processing)**: Even if our AI isn't perfect, we implement a robust Minimum Spanning Tree (MST) or A* heuristic in the Graph Module to bridge small gaps between endpoints. This ensures a mathematically continuous graph—a massive advantage over raw AI outputs.
3. **Spatially-Correlated Disruption Simulation**: Most teams will simulate disaster by randomly deleting 5% of nodes. We will implement a "Flood" or "Earthquake" bounding-box selector. When drawn on the map, all nodes in that radius fail simultaneously. This is mathematically simple to implement but physically realistic and highly impressive to Disaster Management experts.
4. **Topology-Aware Loss Function (clDice)**: Implementing centerline-Dice (clDice) loss during model fine-tuning. It requires very little extra code but forces the AI to prioritize connectivity over pixel thickness, directly addressing the "broken masks" complaint in the problem statement.
