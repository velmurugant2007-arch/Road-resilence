# Architecture Planning Document

> ⚠️ **IMPORTANT**: This is NOT the final architecture. This is a pre-architecture planning and validation document. Actual High-Level Design (HLD) and Low-Level Design (LLD) will only be generated after the official ISRO explanation video is analyzed and all requirements are verified.

## 1. Architecture Goals
- **Mathematical Correctness**: Guarantee a continuous topological graph structure rather than just a visually appealing mask.
- **Occlusion Robustness**: Ensure the AI pipeline prioritizes continuity over pixel precision under clouds/shadows.
- **Demo Viability (Zero-Latency)**: Decouple heavy $O(VE)$ graph processing from the live dashboard to ensure instant interaction during judging.
- **ISRO-Grade Modularity**: Maintain strict boundaries between AI, GIS, Graph, and Visualization modules to allow isolated testing and swapping.

## 2. Engineering Constraints
- **Time Constraint**: Hackathon duration requires strict adherence to MVPs (Minimum Viable Products).
- **Compute Constraint**: Live centrality computation on a full city graph is infeasible on standard hackathon hardware.
- **Data Constraint**: We are constrained by the availability and quality of open-source satellite imagery for Indian metropolises.

## 3. Assumptions
- Assume the evaluation focuses on the *utility* of the graph (routing/resilience) rather than just standard CV metrics (mIoU).
- Assume "Multi-source Urban Data" (from the diagram) is a hint for future expansion, but Optical satellite imagery is sufficient for the MVP.
- Assume the interactive "Hero City" strategy is acceptable in lieu of live arbitrary large-scale city processing.

## 4. Open Questions
- Does the official video define a specific topological loss function we are expected to use?
- Does the official video specify the exact disruption scenarios (e.g., node removal vs. edge removal)?
- Is there a specific Indian metropolis required for the demo, or can we choose Bengaluru?
- What are the exact performance thresholds (e.g., inference speed) expected?

## 5. Components That Are Confirmed
- **Context-Aware Semantic Segmentation Model**: (e.g., UNet with advanced backbone or SegFormer).
- **Graph Construction Module**: Vectorization and Topological Cleaning (MST heuristic).
- **Graph Analysis Engine**: Computation of BC, CFFBC, a-Centrality, and k-Core.
- **Resilience Dashboard**: Giant Component Size tracking and disruption simulation.

## 6. Components Awaiting Confirmation (From Video)
- Specific Loss Functions (e.g., clDice).
- Exact rules for the Disruption Simulation (random vs. spatially correlated).
- Requirements for Multi-modal data fusion (SAR/LiDAR).
- Specific datasets expected to be used.

## 7. Possible Architectural Alternatives & Risks

### Alternative 1: Synchronous Monolith (Live Processing)
- **Description**: Frontend requests an area -> Backend runs AI -> Backend runs Graph -> Backend calculates Centrality -> Frontend displays.
- **Risks**: Extremely high latency. Highly likely to timeout during demo.

### Alternative 2: Asynchronous Pre-computation (Hero City)
- **Description**: Run AI and Centrality offline. Dashboard only serves pre-computed data and handles localized disruption mathematics in the browser or via fast API.
- **Risks**: Less flexible if judges ask to upload a massive, novel image on the spot.

### Alternative 3: Direct-to-Graph AI (e.g., Sat2Graph)
- **Description**: Bypass pixel masks entirely and use an AI model that directly outputs a graph vector.
- **Risks**: High implementation complexity; models are difficult to train and stabilize within a hackathon timeframe.

## 8. Expected Interactions Between Modules
1. **Frontend -> Backend**: Standard REST (or WebSocket) for disruption bounding boxes.
2. **Backend -> GIS**: Fetching pre-processed satellite tiles.
3. **GIS -> AI**: Passing normalized tensors.
4. **AI -> Graph**: Passing raw binary masks (or probability maps).
5. **Graph -> Backend**: Returning serialized NetworkX topologies (GeoJSON) and centrality metrics.
