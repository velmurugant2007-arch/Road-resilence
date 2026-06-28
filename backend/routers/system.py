from fastapi import APIRouter, status
from backend.models.schemas import HealthResponse, SystemConfig
from backend.services.manager import service_manager

router = APIRouter(tags=["System & Configuration"])


@router.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK, summary="Health check endpoint")
@router.get("/api/v1/health", response_model=HealthResponse, status_code=status.HTTP_200_OK, summary="Health check endpoint (v1)")
async def get_health():
    """Returns system health, version, and module initialization statuses."""
    return service_manager.get_health_status()


@router.get("/api/v1/config", response_model=SystemConfig, status_code=status.HTTP_200_OK, summary="Get current system configuration")
async def get_config():
    """Retrieves current global system parameters and thresholds."""
    return service_manager.get_config()


@router.put("/api/v1/config", response_model=SystemConfig, status_code=status.HTTP_200_OK, summary="Update system configuration")
async def update_config(config: SystemConfig):
    """Updates runtime parameters such as AI confidence thresholds or RDP simplification tolerances."""
    return service_manager.update_config(config)
