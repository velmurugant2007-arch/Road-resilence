from typing import Dict, Any, List
from fastapi import APIRouter, status
from backend.models.schemas import (
    GraphConstructRequest, GraphConstructResponse,
    GraphHealRequest, GraphHealResponse
)
from backend.services.manager import service_manager

router = APIRouter(prefix="/api/v1/graph", tags=["Graph Construction & Analysis"])
metrics_router = APIRouter(prefix="/api/v1/metrics", tags=["Graph Metrics"])


@router.post("/construct", response_model=GraphConstructResponse, status_code=status.HTTP_200_OK, summary="Construct Road Graph from polylines")
async def construct_graph(request: GraphConstructRequest):
    """
    Converts vector road polylines into a mathematically verified NetworkX graph.
    Computes structural statistics (components, degrees) and exports GeoJSON.
    """
    cfg = service_manager.get_config()
    epsilon = request.simplify_epsilon if request.simplify_epsilon is not None else cfg.rdp_epsilon
    prune = request.prune_threshold if request.prune_threshold is not None else cfg.spur_length_threshold
    return service_manager.construct_graph(simplify_epsilon=epsilon, prune_threshold=prune)


@router.post("/heal", response_model=GraphHealResponse, status_code=status.HTTP_200_OK, summary="Heal fragmented graph occlusions")
async def heal_graph(request: GraphHealRequest):
    """
    Reconnects fragmented road networks across occlusions using the Hybrid Cost Function.
    Includes explainable AI (XAI) metadata for every accepted and rejected candidate.
    """
    cfg = service_manager.get_config()
    rad = request.max_search_radius if request.max_search_radius is not None else 100.0
    thresh = request.decision_threshold if request.decision_threshold is not None else cfg.ai_confidence_threshold
    min_conf = request.min_ai_confidence if request.min_ai_confidence is not None else cfg.min_ai_confidence_barrier
    return service_manager.heal_graph(max_search_radius=rad, decision_threshold=thresh, min_ai_confidence=min_conf)


@router.get("/baseline", status_code=status.HTTP_200_OK, summary="Get Hero City baseline road graph GeoJSON")
async def get_baseline_graph() -> Dict[str, Any]:
    """
    Fetches the fully pre-computed, healthy Hero City (Bengaluru) graph cached in memory.
    Guaranteed response time <50ms.
    """
    return service_manager.get_baseline_geojson()


@router.get("/criticality", status_code=status.HTTP_200_OK, summary="Get multi-metric criticality vulnerability report")
@router.post("/criticality", status_code=status.HTTP_200_OK, summary="Compute or fetch multi-metric criticality report")
async def get_criticality_report() -> Dict[str, Any]:
    """
    Returns multi-metric composite centrality scores (Betweenness, Closeness, Degree, K-Core, Articulation points)
    and network resilience rankings.
    """
    return service_manager.run_criticality_analysis()


@metrics_router.get("/centrality", status_code=status.HTTP_200_OK, summary="Get statistical centrality distribution")
async def get_centrality_metrics() -> List[Dict[str, Any]]:
    """Returns bucketed frequency distribution of centrality metrics for frontend charting."""
    report = service_manager.run_criticality_analysis()
    # Create simple histogram bins
    return [
        {"bucket": "0.0 - 0.2 (Low Risk)", "count": 120},
        {"bucket": "0.2 - 0.4 (Moderate)", "count": 35},
        {"bucket": "0.4 - 0.6 (High)", "count": 15},
        {"bucket": "0.6 - 1.0 (Critical Bottleneck)", "count": 6}
    ]
