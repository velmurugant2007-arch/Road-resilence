from typing import Dict, Any
from fastapi import APIRouter, status
from backend.models.schemas import DisasterSimulationRequest, DisasterSimulationResponse
from backend.services.manager import service_manager

router = APIRouter(prefix="/api/v1/simulation", tags=["Stress Simulation & Resilience"])


@router.post("/disrupt", response_model=DisasterSimulationResponse, status_code=status.HTTP_200_OK, summary="Simulate regional or stochastic infrastructure disaster")
@router.post("/stress", response_model=DisasterSimulationResponse, status_code=status.HTTP_200_OK, summary="Simulate stress failure scenario")
async def simulate_disaster(request: DisasterSimulationRequest):
    r"""
    Mutates road network topology by removing nodes or edges within a bounding box or stochastically.
    Computes global efficiency drops ($E$), connectivity ratio, travel impact detour %,
    and recommends ranked emergency repair priorities based on marginal recovery ($\Delta R$).
    """
    bbox_dict = None
    if request.bounding_box:
        bbox_dict = {
            "min_lat": request.bounding_box.min_lat,
            "max_lat": request.bounding_box.max_lat,
            "min_lon": request.bounding_box.min_lon,
            "max_lon": request.bounding_box.max_lon
        }
    
    frac = request.failure_fraction if request.failure_fraction is not None else 0.15
    return service_manager.simulate_disaster(
        disaster_type=request.disaster_type,
        bbox=bbox_dict,
        failure_fraction=frac
    )
