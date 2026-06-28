# ATLAS Road Resilience API — Endpoint Documentation

**Version:** 1.0.0  
**Base URL:** `http://localhost:8000/api/v1`  
**OpenAPI Spec:** `docs/openapi.json`  
**Interactive Docs:** `/docs` (Swagger UI) & `/redoc`

---

## Architecture Overview
The ATLAS Backend API is built on high-performance **FastAPI** to serve real-time analytics, explainable AI road repairs, and interactive urban disaster simulations to the interactive frontend dashboard. In strict alignment with design principles, the API acts as a responsive serving layer over pre-computed baseline graph states ("Hero City") while executing rapid geometric filtering and network disruption modeling in memory.

---

## 1. System & Configuration

### `GET /api/v1/health` (also `/health`)
Returns current server lifecycle status, API version, timestamp, and initialization readiness of GIS, AI, and Graph engines.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-06-28T16:30:00Z",
  "modules_initialized": {
    "gis": true,
    "ai": true,
    "graph": true
  }
}
```

### `GET /api/v1/config`
Retrieves global system runtime parameters and algorithm thresholds.

**Response (200 OK):**
```json
{
  "ai_confidence_threshold": 0.65,
  "min_ai_confidence_barrier": 0.30,
  "rdp_epsilon": 2.0,
  "spur_length_threshold": 15.0,
  "criticality_weights": {
    "betweenness": 0.30,
    "closeness": 0.20,
    "degree": 0.15,
    "eigenvector": 0.15,
    "kcore": 0.10,
    "articulation": 0.10
  }
}
```

### `PUT /api/v1/config`
Updates runtime parameters dynamically without server restart.

---

## 2. AI Inference

### `POST /api/v1/ai/infer`
Triggers AI road segmentation and synthetic cloud occlusion generation over target satellite tiles.

**Request Body:**
```json
{
  "image_id": "bengaluru_flood_01",
  "occlusion_type": "cloud",
  "confidence_threshold": 0.65
}
```

**Response (200 OK):**
```json
{
  "status": "success",
  "image_id": "bengaluru_flood_01",
  "inference_time_ms": 12.4,
  "cldice_score": 0.842,
  "iou_score": 0.781,
  "occlusion_coverage_pct": 14.5,
  "message": "AI inference completed successfully."
}
```

---

## 3. Graph Construction & Analysis

### `POST /api/v1/graph/construct`
Converts skeletonized road raster masks into vector polylines and mathematical graph topology.

### `POST /api/v1/graph/heal`
Reconnects fragmented road networks across cloud occlusions using the approved Hybrid Cost Function ($W_1 \cdot \text{Dist} + W_2 \cdot \text{AI} + \dots$). Includes explainable XAI metadata for every evaluated candidate connection.

### `GET /api/v1/graph/baseline`
Returns pre-computed Hero City (Bengaluru) grid road network as standard GeoJSON FeatureCollection guaranteed under 50ms latency.

### `GET /api/v1/graph/criticality`
Executes composite centrality vulnerability ranking (Betweenness, Closeness, Degree, K-Core, Articulation bridges).

### `GET /api/v1/metrics/centrality`
Returns bucketed centrality risk distributions formatted for direct frontend charting.

---

## 4. Stress Simulation & Disaster Resilience

### `POST /api/v1/simulation/disrupt` (also `/stress`)
Simulates stochastic or geographically bounded infrastructure disasters (floods, earthquakes, landslides). Removes nodes/edges and calculates efficiency drop ($E$), travel detour impacts, and recommended emergency repair priority queues based on marginal resilience gain ($\Delta R$).

**Request Body:**
```json
{
  "disaster_type": "flood",
  "bounding_box": {
    "min_lat": 12.91,
    "max_lat": 12.93,
    "min_lon": 77.51,
    "max_lon": 77.53
  },
  "failure_fraction": 0.15
}
```

**Error Handling (422 Unprocessable Entity):**
If the requested bounding box spans more than 0.20 degrees (approx 22km), the server aborts computation to prevent UI browser hangs:
```json
{
  "status": "error",
  "error_type": "BoundingBoxTooLargeError",
  "message": "Requested bounding box span exceeds maximum allowable threshold (0.20 degrees)."
}
```

---

## 5. Data Export

### `GET /api/v1/export/geojson`
Exports active graph topology (baseline or healed state) as standard GeoJSON FeatureCollection compatible with QGIS, Mapbox GL JS, and Leaflet.
