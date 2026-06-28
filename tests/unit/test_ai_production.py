import pytest
import torch
import numpy as np
from pathlib import Path
import shutil
from ai.models.segformer import SegFormerRoadExtractor
from ai.checkpoint import CheckpointManager, CheckpointState
from ai.inference import RoadInferencePipeline, InferenceResult
from ai.model_config import load_config


TEMP_CKPT_DIR = Path("temp_test_ckpt")


@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    TEMP_CKPT_DIR.mkdir(exist_ok=True)
    yield
    shutil.rmtree(TEMP_CKPT_DIR, ignore_errors=True)


def test_config_loads():
    config = load_config()
    assert config.model.name == "SegFormerRoadExtractor"
    assert config.training.amp_enabled is True
    assert config.inference.output_probability_map is True
    assert config.inference.output_binary_mask is True


def test_checkpoint_save_and_load():
    model = SegFormerRoadExtractor()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)

    mgr = CheckpointManager(TEMP_CKPT_DIR, monitor_metric="val_cldice", monitor_mode="max")

    state = CheckpointState(
        epoch=5,
        model_state_dict=model.state_dict(),
        optimizer_state_dict=optimizer.state_dict(),
        scheduler_state_dict=None,
        scaler_state_dict=None,
        best_metric=0.85,
        config={"test": True},
    )

    mgr.save_latest(state)
    assert (TEMP_CKPT_DIR / "latest.pt").exists()

    loaded = mgr.load("latest")
    assert loaded is not None
    assert loaded["epoch"] == 5


def test_checkpoint_best_improvement():
    mgr = CheckpointManager(TEMP_CKPT_DIR, monitor_metric="val_cldice", monitor_mode="max")
    model = SegFormerRoadExtractor()
    state = CheckpointState(
        epoch=10, model_state_dict=model.state_dict(),
        optimizer_state_dict={}, scheduler_state_dict=None,
        scaler_state_dict=None, best_metric=0.0, config={},
    )

    improved = mgr.save_best(state, current_metric=0.90)
    assert improved is True
    assert (TEMP_CKPT_DIR / "best.pt").exists()

    not_improved = mgr.save_best(state, current_metric=0.80)
    assert not_improved is False


def test_inference_dual_output():
    model = SegFormerRoadExtractor()
    pipeline = RoadInferencePipeline(model=model, device="cpu")

    tile = np.random.randint(0, 255, (3, 256, 256), dtype=np.uint8)
    result = pipeline.predict_tile(tile)

    assert isinstance(result, InferenceResult)
    assert result.probability_map.shape == (256, 256)
    assert result.binary_mask.shape == (256, 256)
    assert result.probability_map.dtype == np.float32
    assert result.binary_mask.dtype == np.uint8
    assert set(np.unique(result.binary_mask)).issubset({0, 1})
    assert 0.0 <= result.probability_map.min()
    assert result.probability_map.max() <= 1.0


def test_inference_batch():
    model = SegFormerRoadExtractor()
    pipeline = RoadInferencePipeline(model=model, device="cpu")

    tiles = [np.random.randint(0, 255, (3, 256, 256), dtype=np.uint8) for _ in range(3)]
    results = pipeline.predict_batch(tiles)

    assert len(results) == 3
    for r in results:
        assert r.probability_map.shape == (256, 256)
        assert r.binary_mask.shape == (256, 256)
