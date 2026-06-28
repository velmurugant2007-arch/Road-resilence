import pytest
import torch
from ai.loss.bce import WeightedBCELoss
from ai.loss.dice import DiceLoss
from ai.loss.soft_skeleton import SoftSkeletonize
from ai.loss.cldice import CLDiceLoss
from ai.loss.combined import CombinedLoss
from ai.model_config import LossConfig


# ── Fixtures ──────────────────────────────────────────────────────────

@pytest.fixture
def perfect_prediction():
    """Logits that sigmoid to ~1.0 where target is 1, ~0.0 where target is 0."""
    target = torch.zeros(1, 1, 64, 64)
    target[:, :, 20:44, 30:34] = 1.0  # Vertical road strip
    logits = torch.where(target == 1.0, torch.tensor(5.0), torch.tensor(-5.0))
    return logits, target


@pytest.fixture
def imperfect_prediction():
    """Logits with a gap in the middle of the road (topology break)."""
    target = torch.zeros(1, 1, 64, 64)
    target[:, :, 10:54, 30:34] = 1.0  # Full road
    logits = torch.where(target == 1.0, torch.tensor(5.0), torch.tensor(-5.0))
    logits[:, :, 30:36, 30:34] = -5.0  # Break in the middle
    return logits, target


# ── BCE Tests ─────────────────────────────────────────────────────────

def test_bce_loss_scalar(perfect_prediction):
    logits, target = perfect_prediction
    loss = WeightedBCELoss()(logits, target)
    assert loss.dim() == 0  # Scalar
    assert loss.item() >= 0


def test_bce_loss_perfect_is_low(perfect_prediction):
    logits, target = perfect_prediction
    loss = WeightedBCELoss()(logits, target)
    assert loss.item() < 0.1


# ── Dice Tests ────────────────────────────────────────────────────────

def test_dice_loss_perfect(perfect_prediction):
    logits, target = perfect_prediction
    loss = DiceLoss()(logits, target)
    assert loss.item() < 0.05  # Near-perfect overlap


def test_dice_loss_worst():
    """No overlap at all."""
    target = torch.zeros(1, 1, 64, 64)
    target[:, :, :32, :] = 1.0
    logits = torch.full((1, 1, 64, 64), -5.0)
    logits[:, :, 32:, :] = 5.0  # Predict the opposite half
    loss = DiceLoss()(logits, target)
    assert loss.item() > 0.9


# ── Soft Skeleton Tests ──────────────────────────────────────────────

def test_soft_skeleton_output_shape():
    skel = SoftSkeletonize(num_iterations=10)
    x = torch.rand(2, 1, 64, 64)
    out = skel(x)
    assert out.shape == (2, 1, 64, 64)


def test_soft_skeleton_bounded():
    skel = SoftSkeletonize(num_iterations=10)
    x = torch.rand(1, 1, 64, 64)
    out = skel(x)
    assert out.min() >= 0.0
    assert out.max() <= 1.0


def test_soft_skeleton_thinner_than_input():
    """Skeleton should have fewer active pixels than the original thick mask."""
    skel = SoftSkeletonize(num_iterations=10)
    mask = torch.zeros(1, 1, 64, 64)
    mask[:, :, 20:44, 25:39] = 1.0  # Thick rectangle
    skeleton = skel(mask)
    assert skeleton.sum() < mask.sum()


def test_soft_skeleton_differentiable():
    """Gradients must flow through for clDice training."""
    skel = SoftSkeletonize(num_iterations=10)
    x = torch.rand(1, 1, 32, 32, requires_grad=True)
    out = skel(x)
    loss = out.sum()
    loss.backward()
    assert x.grad is not None
    assert x.grad.abs().sum() > 0


# ── clDice Tests ─────────────────────────────────────────────────────

def test_cldice_perfect_is_low(perfect_prediction):
    logits, target = perfect_prediction
    loss = CLDiceLoss(num_iterations=10)(logits, target)
    assert loss.item() < 0.3  # Should be low for good match


def test_cldice_penalizes_topology_break(perfect_prediction, imperfect_prediction):
    """A broken road should have HIGHER clDice loss than a continuous one."""
    _, target = perfect_prediction
    logits_good, _ = perfect_prediction
    logits_broken, _ = imperfect_prediction
    
    cldice = CLDiceLoss(num_iterations=10)
    loss_good = cldice(logits_good, target)
    loss_broken = cldice(logits_broken, target)
    
    assert loss_broken.item() > loss_good.item(), \
        f"clDice should penalize breaks: good={loss_good.item():.4f}, broken={loss_broken.item():.4f}"


def test_cldice_differentiable():
    logits = torch.randn(1, 1, 64, 64, requires_grad=True)
    target = torch.zeros(1, 1, 64, 64)
    target[:, :, 20:44, 30:34] = 1.0
    loss = CLDiceLoss(num_iterations=5)(logits, target)
    loss.backward()
    assert logits.grad is not None


# ── Combined Loss Tests ──────────────────────────────────────────────

def test_combined_returns_all_components(perfect_prediction):
    logits, target = perfect_prediction
    config = LossConfig(dice_weight=0.5, cldice_weight=0.5)
    loss_fn = CombinedLoss(config)
    result = loss_fn(logits, target)
    
    assert "total" in result
    assert "bce" in result
    assert "dice" in result
    assert "cldice" in result
    assert result["total"].requires_grad  # Only total needs gradients


def test_combined_config_driven():
    """Verify weights from config affect the total."""
    config_a = LossConfig(dice_weight=1.0, cldice_weight=0.0)
    config_b = LossConfig(dice_weight=0.0, cldice_weight=1.0)
    
    logits = torch.randn(1, 1, 32, 32)
    target = torch.zeros(1, 1, 32, 32)
    target[:, :, 10:22, 14:18] = 1.0
    
    result_a = CombinedLoss(config_a)(logits, target)
    result_b = CombinedLoss(config_b)(logits, target)
    
    # With dice_weight=1.0, total should equal dice
    assert abs(result_a["total"].item() - result_a["dice"].item()) < 0.01
