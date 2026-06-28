# API Design

**Project**: ATLAS — Route Resilience
**Status**: APPROVED

---

## 1. API Philosophy
The API is strictly designed to serve the live interactive dashboard. It does not handle heavy AI inference or $O(VE)$ centrality computation; it only serves pre-computed data and performs fast geometric filtering.

## 2. Endpoints

### `GET /api/v1/graph/baseline`
- **Purpose**: Fetches the fully pre-computed, healthy "Hero City" graph.
- **Inputs**: None.
- **Outputs**: `GeoJSON` FeatureCollection of the entire city.
- **Performance**: Cached in memory. Returns in $<50ms$.

### `POST /api/v1/simulation/disrupt`
- **Purpose**: Simulates a disaster (e.g., flood) within a given bounding box and returns the degraded graph and resilience score.
- **Inputs** (JSON):
  ```json
  {
    "disaster_type": "flood",
    "bounding_box": {
      "min_lat": 12.90,
      "max_lat": 12.95,
      "min_lon": 77.50,
      "max_lon": 77.55
    }
  }
  ```
- **Outputs** (JSON):
  ```json
  {
    "status": "success",
    "resilience_score": 0.82,
    "nodes_lost": 450,
    "edges_lost": 520,
    "degraded_graph": { "type": "FeatureCollection", "features": [...] }
  }
  ```
- **Error Handling**: Returns `400 Bad Request` if coordinates are outside the Hero City bounds. Returns `422 Unprocessable Entity` if the bounding box is physically too large (preventing memory crashes).

### `GET /api/v1/metrics/centrality`
- **Purpose**: Returns statistical distributions of the centrality metrics for charting (e.g., histogram of bottleneck severity).
- **Inputs**: None.
- **Outputs**: JSON array of bucketed centrality frequencies.

## 3. Versioning & Authentication
- **Versioning**: All endpoints are prefixed with `/api/v1/` to allow future expansion (e.g., `/v2/` for live AI processing).
- **Authentication**: Intentionally omitted. This is a local hackathon demonstration tool, not a public SaaS platform. Adding JWTs adds zero engineering value to the PS-4 requirements.
