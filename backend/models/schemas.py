from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(..., json_schema_extra={"example": "healthy"})
    version: str = Field(..., json_schema_extra={"example": "1.0.0"})
    timestamp: str = Field(...)
    modules_initialized: Dict[str, bool] = Field(...)


class SystemConfig(BaseModel):
    ai_confidence_threshold: float = Field(0.65, ge=0.0, le=1.0)
    min_ai_confidence_barrier: float = Field(0.30, ge=0.0, le=1.0)
    rdp_epsilon: float = Field(2.0, ge=0.1)
    spur_length_threshold: float = Field(15.0, ge=0.0)
    criticality_weights: Dict[str, float] = Field(
        default_factory=lambda: {
            "betweenness": 0.30,
            "closeness": 0.20,
            "degree": 0.15,
            "eigenvector": 0.15,
            "kcore": 0.10,
            "articulation": 0.10
        }
    )


class AIInferenceRequest(BaseModel):
    image_id: Optional[str] = Field("sample_cloud_01", description="Identifier of image or synthetic scenario")
    occlusion_type: Optional[str] = Field("cloud", description="Type of synthetic occlusion applied")
    confidence_threshold: Optional[float] = Field(0.65, ge=0.0, le=1.0)


class AIInferenceResponse(BaseModel):
    status: str = "success"
    image_id: str
    inference_time_ms: float
    cldice_score: float
    iou_score: float
    occlusion_coverage_pct: float
    message: str


class GraphConstructRequest(BaseModel):
    source_mask_id: Optional[str] = Field("default_mask")
    simplify_epsilon: Optional[float] = Field(2.0)
    prune_threshold: Optional[float] = Field(15.0)


class GraphConstructResponse(BaseModel):
    status: str = "success"
    node_count: int
    edge_count: int
    connected_components: int
    average_degree: float
    geojson: Dict[str, Any]


class GraphHealRequest(BaseModel):
    max_search_radius: Optional[float] = Field(100.0, gt=0.0)
    decision_threshold: Optional[float] = Field(0.65, ge=0.0, le=1.0)
    min_ai_confidence: Optional[float] = Field(0.30, ge=0.0, le=1.0)


class RepairExplanationModel(BaseModel):
    repair_id: Optional[str] = None
    edge_id: Optional[str] = None
    source_node: Any
    destination_node: Any
    distance: float
    ai_confidence: float
    direction_consistency: float
    road_width_similarity: float
    local_road_density: float
    hybrid_cost_score: float
    decision_threshold: float
    status: Optional[str] = None
    accepted: bool
    barrier_veto: Optional[bool] = False
    explanation: str


class GraphHealResponse(BaseModel):
    status: str = "success"
    repaired_gap_count: int
    total_candidates_evaluated: int
    false_connections_prevented: int
    healed_geojson: Dict[str, Any]
    explanations: List[RepairExplanationModel]


class BoundingBox(BaseModel):
    min_lat: float = Field(..., json_schema_extra={"example": 12.90})
    max_lat: float = Field(..., json_schema_extra={"example": 12.95})
    min_lon: float = Field(..., json_schema_extra={"example": 77.50})
    max_lon: float = Field(..., json_schema_extra={"example": 77.55})


class DisasterSimulationRequest(BaseModel):
    disaster_type: str = Field("flood", json_schema_extra={"example": "flood"})
    bounding_box: Optional[BoundingBox] = None
    failure_fraction: Optional[float] = Field(0.15, ge=0.0, le=1.0)
    center_node_id: Optional[Any] = None
    radius_meters: Optional[float] = Field(50.0, gt=0.0)


class RepairPriorityItem(BaseModel):
    priority_rank: int
    element_type: str
    element_id: Any
    estimated_resilience_improvement: float


class DisasterSimulationResponse(BaseModel):
    status: str = "success"
    resilience_score: float
    baseline_resilience_score: float
    nodes_lost: int
    edges_lost: int
    connected_components: int
    connectivity_ratio: float
    travel_impact_pct: float
    degraded_graph: Dict[str, Any]
    recommended_repair_priority: List[RepairPriorityItem]
