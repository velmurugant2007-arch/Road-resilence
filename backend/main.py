import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.logger import get_logger

# Import core exception handlers
from backend.core.exceptions import (
    GraphNotInitializedError, graph_not_initialized_handler,
    BoundingBoxTooLargeError, bounding_box_too_large_handler,
    SimulationExecutionError, simulation_error_handler,
    global_exception_handler
)

# Import routers
from backend.routers import system, ai, graph, simulation, export

logger = get_logger("backend.main")

app = FastAPI(
    title="ATLAS Road Resilience API",
    description="Production FastAPI backend serving AI Road Segmentation, Graph Healing, Criticality Analysis, and Stress Simulation for urban mobility resilience.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware for Frontend Dashboard integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers
app.add_exception_handler(GraphNotInitializedError, graph_not_initialized_handler)
app.add_exception_handler(BoundingBoxTooLargeError, bounding_box_too_large_handler)
app.add_exception_handler(SimulationExecutionError, simulation_error_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Include Routers
app.include_router(system.router)
app.include_router(ai.router)
app.include_router(graph.router)
app.include_router(graph.metrics_router)
app.include_router(simulation.router)
app.include_router(export.router)


@app.on_event("startup")
async def startup_event():
    logger.info("ATLAS FastAPI Backend starting up... Modules initialized.")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("ATLAS FastAPI Backend shutting down cleanly.")


def dump_openapi_schema(output_path: Path = Path("docs/openapi.json")):
    """Helper script to dump OpenAPI schema to disk for documentation compliance."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(app.openapi(), f, indent=2)
    logger.info(f"OpenAPI specification written to {output_path}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
