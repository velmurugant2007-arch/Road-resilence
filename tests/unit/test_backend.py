import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_health_check_endpoints():
    r1 = client.get("/health")
    assert r1.status_code == 200
    data1 = r1.json()
    assert data1["status"] == "healthy"
    assert "gis" in data1["modules_initialized"]

    r2 = client.get("/api/v1/health")
    assert r2.status_code == 200
    assert r2.json()["status"] == "healthy"


def test_system_config_endpoints():
    r_get = client.get("/api/v1/config")
    assert r_get.status_code == 200
    cfg = r_get.json()
    assert "ai_confidence_threshold" in cfg

    # Update config
    cfg["ai_confidence_threshold"] = 0.75
    r_put = client.put("/api/v1/config", json=cfg)
    assert r_put.status_code == 200
    assert r_put.json()["ai_confidence_threshold"] == 0.75


def test_ai_inference_endpoint():
    payload = {
        "image_id": "test_cloud_tile_42",
        "occlusion_type": "cloud",
        "confidence_threshold": 0.70
    }
    res = client.post("/api/v1/ai/infer", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["image_id"] == "test_cloud_tile_42"
    assert data["cldice_score"] > 0.0
    assert data["iou_score"] > 0.0


def test_graph_construct_endpoint():
    res = client.post("/api/v1/graph/construct", json={"simplify_epsilon": 2.5})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["node_count"] > 0
    assert data["edge_count"] > 0
    assert "geojson" in data
    assert data["geojson"]["type"] == "FeatureCollection"


def test_graph_heal_endpoint():
    res = client.post("/api/v1/graph/heal", json={"max_search_radius": 150.0, "decision_threshold": 0.60})
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "repaired_gap_count" in data
    assert "explanations" in data
    assert isinstance(data["explanations"], list)


def test_baseline_graph_endpoint():
    res = client.get("/api/v1/graph/baseline")
    assert res.status_code == 200
    data = res.json()
    assert data["type"] == "FeatureCollection"
    assert len(data["features"]) > 0


def test_criticality_endpoints():
    res1 = client.get("/api/v1/graph/criticality")
    assert res1.status_code == 200
    data1 = res1.json()
    assert data1["status"] == "success"
    assert "vulnerability_report" in data1
    assert "top_critical_nodes" in data1

    res2 = client.get("/api/v1/metrics/centrality")
    assert res2.status_code == 200
    data2 = res2.json()
    assert isinstance(data2, list)
    assert len(data2) == 4


def test_simulation_disrupt_random():
    payload = {
        "disaster_type": "flood",
        "failure_fraction": 0.10
    }
    res = client.post("/api/v1/simulation/disrupt", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["resilience_score"] <= data["baseline_resilience_score"]
    assert "recommended_repair_priority" in data
    assert "degraded_graph" in data


def test_simulation_disrupt_bbox():
    payload = {
        "disaster_type": "landslide",
        "bounding_box": {
            "min_lat": 12.91,
            "max_lat": 12.93,
            "min_lon": 77.51,
            "max_lon": 77.53
        }
    }
    res = client.post("/api/v1/simulation/disrupt", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert data["nodes_lost"] >= 0


def test_simulation_bbox_too_large_error():
    payload = {
        "disaster_type": "earthquake",
        "bounding_box": {
            "min_lat": 12.00,
            "max_lat": 13.00,  # 1.0 degree span (>0.20 limit)
            "min_lon": 77.00,
            "max_lon": 78.00
        }
    }
    res = client.post("/api/v1/simulation/disrupt", json=payload)
    assert res.status_code == 422
    data = res.json()
    assert data["status"] == "error"
    assert data["error_type"] == "BoundingBoxTooLargeError"


def test_export_geojson_endpoint():
    res = client.get("/api/v1/export/geojson")
    assert res.status_code == 200
    data = res.json()
    assert data["type"] == "FeatureCollection"
