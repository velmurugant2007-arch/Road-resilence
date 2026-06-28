import torch
from torch.optim.lr_scheduler import _LRScheduler, CosineAnnealingLR, StepLR, ReduceLROnPlateau
from ai.model_config import TrainingConfig
from utils.logger import get_logger

logger = get_logger("ai.training.scheduler")


def build_scheduler(optimizer: torch.optim.Optimizer, config: TrainingConfig):
    """
    Builds the learning rate scheduler driven by configuration hyperparameters.
    
    Args:
        optimizer: Configured PyTorch optimizer.
        config: TrainingConfig containing scheduler type and parameters.
        
    Returns:
        Configured PyTorch LR Scheduler.
    """
    sched_name = config.scheduler.lower()
    params = config.scheduler_params or {}
    
    if sched_name == "cosineannealinglr":
        t_max = params.get("T_max", config.epochs)
        eta_min = float(params.get("eta_min", 1e-7))
        scheduler = CosineAnnealingLR(optimizer, T_max=t_max, eta_min=eta_min)
    elif sched_name == "steplr":
        step_size = params.get("step_size", 30)
        gamma = float(params.get("gamma", 0.1))
        scheduler = StepLR(optimizer, step_size=step_size, gamma=gamma)
    elif sched_name == "reducelronplateau":
        mode = params.get("mode", "max")
        patience = params.get("patience", 5)
        factor = float(params.get("factor", 0.5))
        scheduler = ReduceLROnPlateau(optimizer, mode=mode, patience=patience, factor=factor)
    else:
        logger.warning(f"Unsupported scheduler '{config.scheduler}', defaulting to CosineAnnealingLR.")
        scheduler = CosineAnnealingLR(optimizer, T_max=config.epochs, eta_min=1e-7)
        
    logger.info(f"Initialized {scheduler.__class__.__name__} with params: {params}")
    return scheduler
