# Technical Debt Register

## Project ATLAS — Route Resilience
### Knowledge Base Entry

> This document tracks conscious architectural and engineering decisions that trade long-term scalable perfection for hackathon feasibility. Every item of technical debt must be logged here so it is not forgotten post-hackathon.

---

## Debt Index

| ID | Title | Priority | Status |
|---|---|---|---|
| TD-0001 | Pre-computed "Hero City" Centrality | High | Active |
| TD-0002 | Heuristic MST Gap Bridging | Medium | Active |
| TD-0003 | Optical-Only Architecture (No SAR) | Low (Hackathon) | Active |
| TD-0004 | Synchronous HTTP for Simulation | Low | Active |

---

## Detailed Register

### TD-0001: Pre-computed "Hero City" Centrality

- **Reason**: Computing exact Betweenness Centrality on a full-city graph is $O(VE)$ and will cause the live dashboard to time out during the 5-minute hackathon demo.
- **Risk**: The system will not be able to process an entirely new, arbitrarily large city uploaded live by a judge without severe latency.
- **Impact**: Fails the "live end-to-end processing" test for massive unmapped regions.
- **Mitigation**: We will build a small "Live Tile Sandbox" for uploading single arbitrary tiles, while keeping the pre-computed "Hero City" (Bengaluru) for the heavy interactive simulation.
- **Priority**: High
- **Future Improvement**: Transition to asynchronous message queues (Celery/RabbitMQ) and implement approximation algorithms (e.g., Brandes algorithm variants) or Graph Neural Networks (GNNs) for $O(1)$ dynamic bottleneck prediction.

---

### TD-0002: Heuristic MST Gap Bridging

- **Reason**: Because the AI (even with topological loss) will produce some fragmented masks, we use a Minimum Spanning Tree (MST) distance heuristic in the Graph Module to force connectivity.
- **Risk**: The heuristic is geometrically naive. It might bridge a gap across a physical barrier (e.g., connecting a road straight across a river where no bridge exists) simply because the nodes are physically close.
- **Impact**: Generates "false positive" infrastructure, leading to routing simulations that suggest driving through impossible terrain.
- **Mitigation**: Hardcode a strict, conservative maximum distance threshold (e.g., `< 30 meters`) for the gap-bridging algorithm.
- **Priority**: Medium
- **Future Improvement**: Replace post-processing heuristics with direct-to-vector extraction models (e.g., Sat2Graph) or incorporate Elevation/LiDAR data to validate if a gap bridge is physically possible.

---

### TD-0003: Optical-Only Architecture (No SAR)

- **Reason**: Multi-modal fusion (Optical + Synthetic Aperture Radar) requires precise spatial alignment and complex training pipelines, which exceeds the hackathon time constraints (40h+ task).
- **Risk**: The AI must "hallucinate" roads under large, dense clouds using only geometric context, which is mathematically unstable.
- **Impact**: High error rates in regions with persistent tropical cloud cover (e.g., monsoon season).
- **Mitigation**: Expose the model's softmax confidence scores to the dashboard, visually marking hallucinated roads under clouds as "Low Confidence" edges.
- **Priority**: Low (for hackathon scoring), Critical (for real-world ISRO deployment).
- **Future Improvement**: Implement an early-fusion deep learning architecture that accepts both Optical and SAR bands, as SAR physically penetrates cloud cover.

---

### TD-0004: Synchronous HTTP for Interactive Simulation

- **Reason**: Setting up reliable WebSockets or Server-Sent Events (SSE) across the stack might consume too much development time compared to standard REST APIs.
- **Risk**: The "Interactive Disruption Dashboard" might experience HTTP polling lag when the user clicks to simulate a disaster.
- **Impact**: The UI might feel slightly rigid or stuttery compared to a true real-time engine.
- **Mitigation**: Keep JSON payloads extremely lightweight (only transmitting diffs of the graph state) and optimize the API routing layer.
- **Priority**: Low
- **Future Improvement**: Refactor the API communication layer to use WebSockets (FastAPI WebSockets + React) for true sub-millisecond bidirectional simulation feedback.

---

*This register is maintained by the Senior Software Architect and reviewed during each Phase transition.*
