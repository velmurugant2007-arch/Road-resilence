import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from utils.logger import get_logger

logger = get_logger("ai.model_config")

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "model_config.yaml"


@dataclass
class EncoderConfig:
    variant: str = "MiT-B2"
    embed_dims: list = field(default_factory=lambda: [64, 128, 320, 512])
    num_heads: list = field(default_factory=lambda: [1, 2, 5, 8])
    depths: list = field(default_factory=lambda: [3, 4, 6, 3])
    sr_ratios: list = field(default_factory=lambda: [8, 4, 2, 1])


@dataclass
class DecoderConfig:
    decoder_dim: int = 256


@dataclass
class ModelConfig:
    name: str = "SegFormerRoadExtractor"
    in_channels: int = 3
    num_classes: int = 1
    encoder: EncoderConfig = field(default_factory=EncoderConfig)
    decoder: DecoderConfig = field(default_factory=DecoderConfig)


@dataclass
class LossConfig:
    type: str = "hybrid"
    dice_weight: float = 0.5
    cldice_weight: float = 0.5
    soft_skeleton_iterations: int = 10


@dataclass
class FinetuneConfig:
    enabled: bool = True
    start_epoch: int = 50
    learning_rate: float = 1e-5
    unfreeze_encoder: bool = True


@dataclass
class TrainingConfig:
    epochs: int = 100
    batch_size: int = 4
    tile_size: int = 512
    learning_rate: float = 6e-5
    weight_decay: float = 0.01
    optimizer: str = "AdamW"
    scheduler: str = "CosineAnnealingLR"
    scheduler_params: dict = field(default_factory=lambda: {"T_max": 100, "eta_min": 1e-7})
    amp_enabled: bool = True
    gradient_clip_max_norm: float = 1.0
    loss: LossConfig = field(default_factory=LossConfig)
    train_ratio: float = 0.70
    val_ratio: float = 0.15
    finetune: FinetuneConfig = field(default_factory=FinetuneConfig)


@dataclass
class CheckpointConfig:
    save_dir: str = "models/checkpoints"
    save_best: bool = True
    save_latest: bool = True
    monitor_metric: str = "val_cldice"
    monitor_mode: str = "max"


@dataclass
class InferenceConfig:
    confidence_threshold: float = 0.5
    output_probability_map: bool = True
    output_binary_mask: bool = True


@dataclass
class FullConfig:
    model: ModelConfig = field(default_factory=ModelConfig)
    training: TrainingConfig = field(default_factory=TrainingConfig)
    checkpointing: CheckpointConfig = field(default_factory=CheckpointConfig)
    inference: InferenceConfig = field(default_factory=InferenceConfig)


def load_config(path: Optional[Path] = None) -> FullConfig:
    """
    Loads the model configuration from YAML and returns a typed dataclass.
    Falls back to defaults if the file is missing.
    """
    config_path = path or CONFIG_PATH

    if not config_path.exists():
        logger.warning(f"Config file not found at {config_path}. Using defaults.")
        return FullConfig()

    with open(config_path, "r") as f:
        raw = yaml.safe_load(f)

    # Build typed config from raw dict
    encoder_raw = raw.get("model", {}).get("encoder", {})
    decoder_raw = raw.get("model", {}).get("decoder", {})
    model_raw = raw.get("model", {})
    training_raw = raw.get("training", {})
    loss_raw = training_raw.get("loss", {})
    finetune_raw = training_raw.get("finetune", {})
    ckpt_raw = raw.get("checkpointing", {})
    inf_raw = raw.get("inference", {})

    config = FullConfig(
        model=ModelConfig(
            name=model_raw.get("name", "SegFormerRoadExtractor"),
            in_channels=model_raw.get("in_channels", 3),
            num_classes=model_raw.get("num_classes", 1),
            encoder=EncoderConfig(**{k: v for k, v in encoder_raw.items() if k != "variant" and k in EncoderConfig.__dataclass_fields__},
                                  variant=encoder_raw.get("variant", "MiT-B2")),
            decoder=DecoderConfig(**decoder_raw),
        ),
        training=TrainingConfig(
            epochs=training_raw.get("epochs", 100),
            batch_size=training_raw.get("batch_size", 4),
            tile_size=training_raw.get("tile_size", 512),
            learning_rate=training_raw.get("learning_rate", 6e-5),
            weight_decay=training_raw.get("weight_decay", 0.01),
            optimizer=training_raw.get("optimizer", "AdamW"),
            scheduler=training_raw.get("scheduler", "CosineAnnealingLR"),
            scheduler_params=training_raw.get("scheduler_params", {"T_max": 100, "eta_min": 1e-7}),
            amp_enabled=training_raw.get("amp_enabled", True),
            gradient_clip_max_norm=training_raw.get("gradient_clip_max_norm", 1.0),
            loss=LossConfig(**loss_raw),
            train_ratio=training_raw.get("train_ratio", 0.70),
            val_ratio=training_raw.get("val_ratio", 0.15),
            finetune=FinetuneConfig(**finetune_raw),
        ),
        checkpointing=CheckpointConfig(**ckpt_raw),
        inference=InferenceConfig(**inf_raw),
    )

    logger.info(f"Model config loaded from {config_path}")
    return config
