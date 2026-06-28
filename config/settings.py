import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

# Root directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """
    Centralized Configuration Management for ATLAS.
    Loads from environment variables or a .env file.
    """
    PROJECT_NAME: str = "ATLAS - Route Resilience"
    API_V1_STR: str = "/api/v1"
    
    # Paths
    DATA_DIR: Path = BASE_DIR / "datasets"
    MODELS_DIR: Path = BASE_DIR / "models"
    LOGS_DIR: Path = BASE_DIR / "logs"
    
    # Graph Constants
    MST_MAX_HEALING_DISTANCE_METERS: float = 30.0
    
    # AI Constants
    BATCH_SIZE: int = 4
    TILE_SIZE: int = 512
    
    # Bounding Box Constraints to prevent memory crash
    MAX_SIMULATION_AREA_SQ_KM: float = 25.0

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Global settings instance
settings = Settings()

# Ensure critical directories exist
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.MODELS_DIR, exist_ok=True)
os.makedirs(settings.LOGS_DIR, exist_ok=True)
