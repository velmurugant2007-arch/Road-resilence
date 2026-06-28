import pytest
import torch
from ai.models.segformer import SegFormerRoadExtractor


def test_segformer_output_shape():
    """Model must output (B, 1, H, W) matching input spatial dimensions."""
    model = SegFormerRoadExtractor(in_channels=3, num_classes=1)
    model.eval()
    x = torch.randn(1, 3, 512, 512)
    with torch.no_grad():
        out = model(x)
    assert out.shape == (1, 1, 512, 512), f"Wrong output shape: {out.shape}"


def test_segformer_arbitrary_resolution():
    """SegFormer should handle non-square inputs (no positional encoding dependency)."""
    model = SegFormerRoadExtractor()
    model.eval()
    x = torch.randn(1, 3, 256, 384)
    with torch.no_grad():
        out = model(x)
    assert out.shape == (1, 1, 256, 384), f"Wrong output shape: {out.shape}"


def test_segformer_batch():
    """Batch inference must work."""
    model = SegFormerRoadExtractor()
    model.eval()
    x = torch.randn(2, 3, 256, 256)
    with torch.no_grad():
        out = model(x)
    assert out.shape[0] == 2


def test_segformer_parameter_count():
    """MiT-B2 should have roughly 25-30M parameters. Sanity check."""
    model = SegFormerRoadExtractor()
    params = sum(p.numel() for p in model.parameters())
    assert 10_000_000 < params < 50_000_000, f"Unexpected param count: {params}"
