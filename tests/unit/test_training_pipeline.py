import pytest
import shutil
from pathlib import Path
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

from ai.model_config import FullConfig
from ai.models.segformer import SegFormerRoadExtractor
from ai.training.metrics import RoadMetrics
from ai.training.optimizer import build_optimizer
from ai.training.scheduler import build_scheduler
from ai.training.callbacks import EarlyStopping
from ai.training.validation import Validator
from ai.training.trainer import Trainer
from ai.loss.combined import CombinedLoss


@pytest.fixture
def dummy_data():
    """Generates a tiny dummy dataset of 4 samples (B=4, C=3, H=64, W=64)."""
    images = torch.randn(4, 3, 64, 64)
    masks = torch.randint(0, 2, (4, 1, 64, 64)).float()
    dataset = TensorDataset(images, masks)
    loader = DataLoader(dataset, batch_size=2)
    return loader


@pytest.fixture
def dummy_config():
    config = FullConfig()
    config.training.epochs = 2
    config.training.batch_size = 2
    config.training.tile_size = 64
    config.checkpointing.save_dir = "tests/tmp_checkpoints"
    return config


def test_road_metrics():
    metrics_fn = RoadMetrics(skeleton_iterations=3)
    logits = torch.randn(2, 1, 64, 64)
    targets = torch.randint(0, 2, (2, 1, 64, 64)).float()
    
    res = metrics_fn(logits, targets)
    assert "iou" in res
    assert "dice" in res
    assert "precision" in res
    assert "recall" in res
    assert "f1" in res
    assert "connectivity_ratio" in res
    assert 0.0 <= res["iou"] <= 1.0


def test_optimizer_builder():
    model = nn.Linear(10, 1)
    config = FullConfig().training
    config.optimizer = "AdamW"
    config.learning_rate = 1e-4
    
    opt = build_optimizer(model, config)
    assert isinstance(opt, torch.optim.AdamW)
    assert opt.param_groups[0]["lr"] == 1e-4


def test_scheduler_builder():
    model = nn.Linear(10, 1)
    opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
    config = FullConfig().training
    config.scheduler = "CosineAnnealingLR"
    
    sched = build_scheduler(opt, config)
    assert isinstance(sched, torch.optim.lr_scheduler.CosineAnnealingLR)


def test_early_stopping():
    es = EarlyStopping(patience=2, mode="max")
    assert not es(0.5)
    assert not es(0.4)  # 1 worse
    assert es(0.3)      # 2 worse -> trigger early stop


def test_validator_dry_run(dummy_data):
    model = SegFormerRoadExtractor(in_channels=3, num_classes=1)
    loss_fn = CombinedLoss()
    metrics_fn = RoadMetrics(skeleton_iterations=2)
    device = torch.device("cpu")
    
    val = Validator(loss_fn, metrics_fn, device, amp_enabled=False)
    losses, metrics = val.validate(model, dummy_data)
    
    assert "total" in losses
    assert "iou" in metrics


def test_trainer_one_epoch_dry_run(dummy_data, dummy_config):
    model = SegFormerRoadExtractor(in_channels=3, num_classes=1)
    
    # Run 1 epoch dry-run
    trainer = Trainer(
        model=model,
        train_loader=dummy_data,
        val_loader=dummy_data,
        config=dummy_config,
        log_dir="tests/tmp_logs"
    )
    
    # Disable CUDA AMP for CPU testing
    trainer.amp_enabled = False
    trainer.train(max_epochs=1)
    
    # Verify log output was created
    assert Path("tests/tmp_logs/training_history.csv").exists()
    
    # Cleanup
    shutil.rmtree("tests/tmp_checkpoints", ignore_errors=True)
    shutil.rmtree("tests/tmp_logs", ignore_errors=True)
