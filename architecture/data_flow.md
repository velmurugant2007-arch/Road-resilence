# Data Flow Diagram

## Project ATLAS — Route Resilience

> ⚠️ **Status**: Awaiting Phase 5. End-to-end data pipeline will be documented here.

## Preliminary Data Flow

```
Satellite Image (GeoTIFF)
    ↓ [GIS Module]
CRS Validation → Tiling → Normalization
    ↓ [AI Module]
Per-Tile Inference → Confidence Maps → Binary Masks
    ↓ [GIS Module]
Tile Reassembly → Vectorization → Georeferenced Roads
    ↓ [Graph Module]
Skeletonization → Graph Construction → Topology Healing
    ↓ [Graph Module]
Centrality Analysis → Resilience Simulation → Critical Nodes/Edges
    ↓ [Backend API]
Structured Results → JSON/GeoJSON
    ↓ [Dashboard]
Map Visualization → Interactive Analysis
```

---

*Formal data flow specification: Phase 5*
