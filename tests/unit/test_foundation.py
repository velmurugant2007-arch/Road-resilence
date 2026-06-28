import pytest
from config.settings import settings
from utils.logger import get_logger
import os

def test_settings_initialization():
    """
    Objective: Verify that the centralized configuration system loads correctly.
    """
    assert settings.PROJECT_NAME == "ATLAS - Route Resilience"
    assert settings.API_V1_STR == "/api/v1"
    
    # Ensure directories were created
    assert settings.DATA_DIR.exists()
    assert settings.MODELS_DIR.exists()
    assert settings.LOGS_DIR.exists()

def test_logger_initialization():
    """
    Objective: Verify that the logging framework can instantiate a module-specific logger.
    """
    logger = get_logger("test_module")
    assert logger.name == "atlas.test_module"
    
    # Fire a test log to ensure no exceptions are raised
    logger.info("Test log executed successfully.")
