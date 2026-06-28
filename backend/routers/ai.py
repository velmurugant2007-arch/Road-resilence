from fastapi import APIRouter, status
from backend.models.schemas import AIInferenceRequest, AIInferenceResponse
from backend.services.manager import service_manager

router = APIRouter(prefix="/api/v1/ai", tags=["AI Inference"])


@router.post("/infer", response_model=AIInferenceResponse, status_code=status.HTTP_200_OK, summary="Run AI Road Segmentation & Occlusion Inference")
async def run_inference(request: AIInferenceRequest):
    """
    Executes SegFormer inference over input satellite tiles or synthetic occlusion masks.
    Returns segmentation accuracy metrics (clDice, IoU) and detected occlusion coverage percentage.
    """
    thresh = request.confidence_threshold if request.confidence_threshold is not None else service_manager.get_config().ai_confidence_threshold
    return service_manager.run_ai_inference(
        image_id=request.image_id or "sample_cloud_01",
        occlusion_type=request.occlusion_type or "cloud",
        confidence_threshold=thresh
    )
