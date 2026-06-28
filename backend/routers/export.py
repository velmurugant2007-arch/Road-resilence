from typing import Dict, Any
from fastapi import APIRouter, status
from backend.services.manager import service_manager

router = APIRouter(prefix="/api/v1/export", tags=["Data Export"])


@router.get("/geojson", status_code=status.HTTP_200_OK, summary="Export current graph as standard GeoJSON FeatureCollection")
async def export_geojson() -> Dict[str, Any]:
    """
    Exports current active graph state (baseline or healed) as a standard GeoJSON FeatureCollection
    suitable for QGIS, Mapbox, or Leaflet frontend rendering.
    """
    return service_manager.get_baseline_geojson()
