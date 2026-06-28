# Phase 2 Engineering Review Report

**Date**: 2026-06-26  
**Type**: Internal ISRO Design Review Board  
**Subject**: Review of Phase 2 Problem Statement Analysis (PS-4)  
**Status**: Completed  

---

## Executive Summary: Consolidated Engineering Review

The internal review board consisting of 9 domain experts has analyzed the Phase 2 Problem Statement Deconstruction. The general consensus is that the analysis successfully identified the fundamental shift from pixel-level Computer Vision to Topology-Aware Network Science. However, the review exposed critical blind spots regarding spatial correlation of disasters, computational complexity of centrality metrics, and data modality constraints.

### Critical Action Items (To be addressed in Phase 5 Architecture):
1. **Data Modality**: Deep learning cannot "hallucinate" roads under massive clouds accurately without either **Temporal Data** (time-series imagery) or **SAR Data** (Synthetic Aperture Radar). Architecture must support one of these.
2. **Algorithmic Complexity**: Exact Betweenness Centrality is $O(VE)$. The backend must use approximation algorithms (e.g., Brandes) or pre-compute the graph for the live demo.
3. **Simulation Realism**: Randomly deleting nodes is mathematically sound but physically unrealistic. Disruptions must be spatially correlated (e.g., simulating flood zones or localized localized infrastructural collapse).
4. **Graph Semantics**: The graph cannot treat all edges equally. It must support weighting by road hierarchy (arterial vs. local) and account for informal settlements typical of Indian metropolises.
5. **Demo Strategy**: The hackathon environment requires an MVP. The system will pre-compute a "Hero City" (Bengaluru) to guarantee a zero-latency, interactive "wow factor" for the judges.

---

## 1. ISRO Scientist Review

- **Strengths**: Strict traceability to the problem statement. Systemic view of the pipeline.
- **Weaknesses**: Lacks definition of data constraints (resolution, multi-spectral bands).
- **Missing Requirements**: Ground Sample Distance (GSD) requirements not defined. Over-reliance on "cloud cover" mitigation without specifying sensor types.
- **Incorrect Assumptions**: Assuming optical imagery alone can see through thick clouds. It cannot; it will simply guess based on geometry.
- **Risks**: Indian metropolises have mixed-use zoning, making purely geometric extraction prone to high error rates.
- **Questions**: Will ISRO Cartosat/Resourcesat data be used, or open-source datasets?
- **Suggestions**: Incorporate Synthetic Aperture Radar (SAR) data fusion. SAR physically penetrates clouds.
- **Innovation Opportunities**: Optical + SAR early-fusion architecture.

## 2. Computer Vision Researcher Review

- **Strengths**: Accurate recognition that mIoU is insufficient and `Breaks/km` is critical.
- **Weaknesses**: Vague on the specific "context-aware" mechanisms (e.g., Transformers vs. dilated CNNs).
- **Missing Requirements**: Inference speed and latency requirements are not addressed.
- **Incorrect Assumptions**: Assuming topological loss functions (like clDice) are easy to optimize. They are often highly unstable during backpropagation.
- **Risks**: Training heavily penalizing topology might degrade pixel-level precision, leading to wide, blurry roads.
- **Questions**: How will ground truth datasets with realistic occlusions be sourced or annotated?
- **Suggestions**: Use a multi-task learning approach (predicting segmentation mask + edge orientation/direction vectors) to implicitly aid topology without unstable loss functions.
- **Innovation Opportunities**: Differentiable graph rendering during the training loop.

## 3. GIS Engineer Review

- **Strengths**: Explicit identification of the "mathematically continuous" necessity.
- **Weaknesses**: Glosses over Coordinate Reference System (CRS) challenges and vector geometry operations.
- **Missing Requirements**: Vector simplification and spatial indexing (e.g., PostGIS) not specified.
- **Incorrect Assumptions**: Mask-to-graph conversion is treated as a trivial post-processing step. It is highly complex in dense, irregular urban areas.
- **Risks**: Skeletonization algorithms often create artificial "spurs" or false loops that ruin routing logic.
- **Questions**: What spatial resolution is assumed for the vectorization?
- **Suggestions**: Implement the Douglas-Peucker algorithm for vector simplification and a strict spur-pruning heuristic.
- **Innovation Opportunities**: Direct-to-vector road extraction models (e.g., Sat2Graph) bypassing raster masks entirely.

## 4. Graph Theory Expert Review

- **Strengths**: Correct identification of required centrality metrics (BC, k-Core, etc.).
- **Weaknesses**: Fails to address the computational complexity of Betweenness Centrality on large urban graphs ($O(VE)$).
- **Missing Requirements**: Graph directionality (one-way streets) and semantic weighting strategies (distance, speed limits) are missing.
- **Incorrect Assumptions**: "Giant Component Size" might be a misleading metric if a city naturally has a river dividing it into two large components.
- **Risks**: Exact centrality computation will time out on a city scale, rendering the dashboard useless.
- **Questions**: Are we treating the graph as directed or undirected?
- **Suggestions**: Use Brandes' algorithm for BC. Use approximate metrics for live dashboard interactions.
- **Innovation Opportunities**: Train Graph Neural Networks (GNNs) to predict bottlenecks dynamically in $O(1)$ time based on pre-computed topologies.

## 5. Senior Software Architect Review

- **Strengths**: The 6-module pipeline approach is logical and decoupled.
- **Weaknesses**: Data transfer bottlenecks between AI (GPU memory) and Graph (CPU RAM) are not considered.
- **Missing Requirements**: System scalability and state management for the simulation module.
- **Incorrect Assumptions**: Assuming a synchronous processing pipeline is fine. Heavy graph tasks will block the API.
- **Risks**: "End-to-end pipeline" might take too long per request for an interactive web dashboard.
- **Questions**: Where does the graph state live during the interactive resilience simulation?
- **Suggestions**: Decouple inference and graph generation via message queues (e.g., Redis/RabbitMQ/Celery).
- **Innovation Opportunities**: Edge computing for tile-based decentralized inference.

## 6. Disaster Management Expert Review

- **Strengths**: Strong focus on urban collapse and resilience tracking.
- **Weaknesses**: Disruption scenarios lack domain context (flood vs. earthquake vs. traffic jam).
- **Missing Requirements**: Temporal dynamics (how fast do roads recover?) and physical vulnerability (bridges fail easier than ground roads).
- **Incorrect Assumptions**: Removing nodes randomly simulates disaster accurately. Disasters are spatially correlated.
- **Risks**: The system identifies a "resilient" alternative route that is practically unusable for emergency vehicles (e.g., a narrow dirt path).
- **Questions**: Can we weight edges by road hierarchy (arterial vs. local)?
- **Suggestions**: Implement spatially-correlated disruptions (e.g., simulating the flooding of a specific low-elevation zone using a bounding box).
- **Innovation Opportunities**: Real-time dynamic re-routing algorithms under cascading failure conditions.

## 7. Urban Planning Expert Review

- **Strengths**: Recognizes fragmentation and stagnation issues in Indian metropolises.
- **Weaknesses**: Doesn't account for informal settlements (slums), which are common and visually indistinguishable from dense housing.
- **Missing Requirements**: Integration with existing master plans or OpenStreetMap (OSM) baselines for verification.
- **Incorrect Assumptions**: Assumes all extracted paths are valid vehicular roads (they might be pedestrian alleyways).
- **Risks**: High false-positive rate in dense areas will misguide traffic simulations.
- **Questions**: How does the system differentiate between a drivable road and a wide paved pedestrian zone from satellite imagery alone?
- **Suggestions**: Cross-reference AI output with OSM data to validate primary arteries, using AI only to discover unmapped local roads.
- **Innovation Opportunities**: Analyzing "unmapped" informal roads to suggest infrastructure upgrades to municipal bodies.

## 8. AI/ML Research Scientist Review

- **Strengths**: Strong focus on occlusion robustness.
- **Weaknesses**: Lack of clarity on synthetic data generation or data augmentation strategies.
- **Missing Requirements**: Domain adaptation strategy. Models trained on US/EU datasets fail catastrophically on Indian urban geometries.
- **Incorrect Assumptions**: Deep learning alone can "see through" large continuous clouds without temporal data.
- **Risks**: Hallucination. The AI might "invent" roads that do not exist under large clouds simply to satisfy the topological loss function.
- **Questions**: Will we use temporal imagery (time-series) to look back at when the cloud wasn't there?
- **Suggestions**: Use spatiotemporal models (analyzing images from $T-1, T, T+1$) to solve cloud occlusion deterministically rather than guessing.
- **Innovation Opportunities**: Spatiotemporal transformers for deterministic cloud-free road extraction.

## 9. Hackathon Judge Review

- **Strengths**: Extreme thoroughness, ISRO-grade documentation, and deep understanding of the problem.
- **Weaknesses**: Danger of over-engineering. The focus might drift from a working demo to theoretical perfection.
- **Missing Requirements**: A clear "wow factor" UX requirement for the live demonstration.
- **Incorrect Assumptions**: Assuming judges will read all 100+ documents. We have 5 minutes to present; they want to see the system *working*.
- **Risks**: Failing to deliver a working end-to-end demo due to spending too much time building microservices or mathematically perfect topologies.
- **Questions**: What is the Minimum Viable Product (MVP) for the 24-hour/48-hour submission?
- **Suggestions**: Build a pre-computed "Hero City" (e.g., Bengaluru) where all heavy AI and Graph processing is done beforehand. Allow the dashboard to perform instant, interactive simulations on this pre-computed graph.
- **Innovation Opportunities**: Gamification of the dashboard—allow judges to "bomb" the city by clicking on the map and watch the graph heal or degrade in real-time.
