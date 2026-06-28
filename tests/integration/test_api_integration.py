import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def test_end_to_end_resilience_workflow():
    """
    Integration test verifying complete end-to-end dashboard integration workflow:
    1. Check health & configuration.
    2. Run AI inference over satellite scenario.
    3. Construct road graph from inferred polylines.
    4. Fetch baseline Hero City graph for initial dashboard view.
    5. Simulate localized flood disruption scenario.
    6. Heal fragmented road network across occlusion gaps.
    7. Export final GeoJSON for visualization.
    """
    # 1. Health & Config
    h_res = client.get("/api/v1/health")
    assert h_res.status_code == 200
    assert h_res.json()["status"] == "healthy"

    # 2. AI Inference
    ai_res = client.post("/api/v1/ai/infer", json={"image_id": "bengaluru_flood_01", "occlusion_type": "cloud"})
    assert ai_res.status_code == 200
    ai_data = ai_res.json()
    assert ai_data["cldice_score"] >= 0.75

    # 3. Graph Construction
    gc_res = client.post("/api/v1/graph/construct", json={"simplify_epsilon": 2.0})
    assert gc_res.status_code == 200
    gc_data = gc_res.json()
    assert gc_data["node_count"] >= 50

    # 4. Baseline Graph
    bg_res = client.get("/api/v1/graph/baseline")
    assert bg_res.status_code == 200
    bg_data = bg_res.json()
    assert bg_data["type"] == "FeatureCollection"

    # 5. Simulate Disaster
    sim_res = client.post("/api/v1/simulation/disrupt", json={
        "disaster_type": "flood",
        "bounding_box": {
            "min_lat": 12.91,
            "max_lat": 12.93,
            "min_lon": 77.51,
            "max_lon": 77.53
        }
    })
    assert sim_res.status_code == 200
    sim_data = sim_res.json()
    assert sim_data["nodes_lost"] >= 0
    assert "recommended_repair_priority" in sim_data

    # 6. Heal Graph
    heal_res = client.post("/api/v1/graph/heal", json={"max_search_radius": 150.0, "decision_threshold": 0.65})
    assert heal_res.status_code == 200
    heal_data = heal_res.json()
    assert heal_data["status"] == "success"
    assert isinstance(heal_data["explanations"], list)

    # 7. Export GeoJSON
    exp_res = client.get("/api/v1/export/geojson")
    assert exp_res.status_code == 200
    assert exp_res.json()["type"] == "FeatureCollection"
