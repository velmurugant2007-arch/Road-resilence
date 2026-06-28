import torch
from torch.optim import Optimizer, AdamW, Adam, SGD
from ai.model_config import TrainingConfig
from utils.logger import get_logger

logger = get_logger("ai.training.optimizer")


def build_optimizer(model: torch.nn.Module, config: TrainingConfig) -> Optimizer:
    """
    Builds the PyTorch optimizer driven by configuration hyperparameters.
    
    Args:
        model: PyTorch model whose parameters will be optimized.
        config: TrainingConfig containing optimizer type, lr, and weight decay.
        
    Returns:
        Configured PyTorch Optimizer.
    """
    opt_name = config.optimizer.lower()
    lr = config.learning_rate
    weight_decay = config.weight_decay
    
    # Separate weight decay for bias and layer norm parameters (best practice for transformers)
    decay_params = []
    no_decay_params = []
    
    for name, param in model.named_parameters():
        if not param.requires_grad:
            continue
        if len(param.shape) == 1 or name.endswith(".bias") or "norm" in name.lower():
            no_decay_params.append(param)
        else:
            decay_params.append(param)
            
    param_groups = [
        {"params": decay_params, "weight_decay": weight_decay},
        {"params": no_decay_params, "weight_decay": 0.0},
    ]
    
    if opt_name == "adamw":
        optimizer = AdamW(param_groups, lr=lr)
    elif opt_name == "adam":
        optimizer = Adam(param_groups, lr=lr)
    elif opt_name == "sgd":
        optimizer = SGD(param_groups, lr=lr, momentum=0.9)
    else:
        logger.warning(f"Unsupported optimizer '{config.optimizer}', defaulting to AdamW.")
        optimizer = AdamW(param_groups, lr=lr)
        
    logger.info(f"Initialized {optimizer.__class__.__name__} optimizer with lr={lr}, weight_decay={weight_decay}")
    return optimizer
