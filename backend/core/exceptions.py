from fastapi import Request, status
from fastapi.responses import JSONResponse
from utils.logger import get_logger

logger = get_logger("backend.core.exceptions")


class GraphNotInitializedError(Exception):
    def __init__(self, message: str = "Graph state is not initialized or empty."):
        self.message = message


class BoundingBoxTooLargeError(Exception):
    def __init__(self, message: str = "Requested bounding box exceeds permitted physical area limits."):
        self.message = message


class SimulationExecutionError(Exception):
    def __init__(self, message: str = "Error executing stress simulation scenario."):
        self.message = message


async def graph_not_initialized_handler(request: Request, exc: GraphNotInitializedError):
    logger.error(f"GraphNotInitializedError on {request.url.path}: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"status": "error", "error_type": "GraphNotInitializedError", "message": exc.message}
    )


async def bounding_box_too_large_handler(request: Request, exc: BoundingBoxTooLargeError):
    logger.warning(f"BoundingBoxTooLargeError on {request.url.path}: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"status": "error", "error_type": "BoundingBoxTooLargeError", "message": exc.message}
    )


async def simulation_error_handler(request: Request, exc: SimulationExecutionError):
    logger.error(f"SimulationExecutionError on {request.url.path}: {exc.message}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"status": "error", "error_type": "SimulationExecutionError", "message": exc.message}
    )


async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception on {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": "error", "error_type": "InternalServerError", "message": "An unexpected server error occurred."}
    )
