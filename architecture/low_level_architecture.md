# Low-Level Design (LLD)

**Project**: ATLAS — Route Resilience
**Status**: APPROVED (Post-CER Revisions)

---

## 1. GIS Preprocessing Module (`gis/`)
- **Purpose**: Prepare spatial data for the AI pipeline.
- **Inputs**: GeoTIFF, CRS definitions.
- **Outputs**: Tensors ($512 \times 512$).
- **Algorithms**: Rasterio windowed reading, **ImageNet Mean/Std Normalization**.
- **Optimization Strategy**: We strictly avoid Min-Max normalization. Data is normalized using ImageNet priors (`mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`) to preserve pre-trained SegFormer weights.

## 2. AI Semantic Segmentation Module (`ai/`)
- **Purpose**: Extract road masks.
- **Algorithms**: SegFormer, clDice Loss (Soft-Skeletonized), Sigmoid Activation.
- **Outputs**: Probability mask, Softmax Confidence Map.
- **Failure Cases**: Overconfident false positives. Mitigated by Confidence Calibration (see AI Architecture doc).

## 3. Graph Construction & Healing Module (`graph/construction.py`)
- **Purpose**: Convert masks to mathematically continuous topologies.
- **Algorithms**: Zhang-Suen Thinning, RDP simplification.
- **CRS Reprojection**: Converts `EPSG:4326` inputs into local UTM to ensure valid metric calculations.
- **Graph Healing**: Replaces basic MST with the **Hybrid Cost Function** (Euclidean, AI Probability, Directional consistency).
- **Optimization Strategy**: Use R-Trees for fast spatial bounding queries when identifying candidate healing pairs.

## 4. Graph Centrality Analysis Module (`graph/analysis.py`)
- **Purpose**: Calculate node/edge importance metrics.
- **Algorithms**: Brandes algorithm for Betweenness Centrality, Batagelj-Zaversnik for k-Core.
- **Optimization Strategy**: Pre-compute offline due to $O(VE)$ complexity.

## 5. Backend Services API (`backend/`)
- **Purpose**: Orchestrate data flow to the dashboard.
- **Outputs**: GeoJSON FeatureCollection.
- **Contingency Strategy**: Initially serves raw GeoJSON. If profiling shows $>100k$ edges causing browser/API timeouts, we will dynamically pivot to serving Vector Tiles (MVT).

## 6. Frontend Disruption Simulator (`dashboard/`)
- **Algorithms**: Turf.js for fast in-browser geometric intersection.
- **Outputs**: Rendered map, Decision Support Panel, Explainability metrics.
