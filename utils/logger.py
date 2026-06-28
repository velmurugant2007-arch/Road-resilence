import logging
import logging.config
import yaml
from pathlib import Path
from config.settings import settings

def setup_logging():
    """
    Initializes the logging configuration from the YAML file.
    Ensures logs are correctly routed to both console and file.
    """
    config_path = Path(__file__).resolve().parent.parent / "config" / "logging.yaml"
    
    if config_path.exists():
        with open(config_path, 'rt') as f:
            config = yaml.safe_load(f)
            
        # Ensure log directory exists as defined in config
        log_file = config.get('handlers', {}).get('file', {}).get('filename')
        if log_file:
            Path(log_file).parent.mkdir(parents=True, exist_ok=True)
            
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=logging.INFO)
        logging.warning("logging.yaml not found. Using default basic config.")

def get_logger(module_name: str) -> logging.Logger:
    """
    Returns a logger for a specific module, standardized across the project.
    """
    return logging.getLogger(f"atlas.{module_name}")
