# Coding Standards

## Project ATLAS — Route Resilience
### Bharatiya Antariksh Hackathon 2026 (ISRO) — PS-4

---

## General Principles

1. **Readability over cleverness** — Code should be understandable by someone unfamiliar with the project
2. **Explicit over implicit** — Name variables, functions, and classes descriptively
3. **No magic numbers** — All constants are named and documented
4. **Error handling** — Every external interaction has error handling
5. **Comments explain why, not what** — Code structure explains what; comments explain reasoning

---

## Python Standards

### Style
- Follow **PEP 8** with a maximum line length of 100 characters
- Use **type hints** for all function signatures
- Use **docstrings** (Google style) for all public functions, classes, and modules

### Naming
```python
# Modules: snake_case
road_segmentation.py

# Classes: PascalCase
class RoadExtractor:

# Functions/Methods: snake_case
def extract_roads(image: np.ndarray) -> np.ndarray:

# Constants: UPPER_SNAKE_CASE
MAX_TILE_SIZE = 512
DEFAULT_CONFIDENCE_THRESHOLD = 0.5

# Private: leading underscore
def _preprocess_tile(tile: np.ndarray) -> np.ndarray:
```

### Documentation
```python
def extract_roads(
    image: np.ndarray,
    confidence_threshold: float = 0.5,
    tile_size: int = 512
) -> np.ndarray:
    """Extract road network from satellite imagery.

    Performs semantic segmentation on the input satellite image to produce
    a binary road mask. Handles tiling internally for large images.

    Args:
        image: Input satellite image as numpy array (H, W, C).
        confidence_threshold: Minimum prediction confidence for road class.
        tile_size: Size of tiles for processing large images.

    Returns:
        Binary road mask as numpy array (H, W) with dtype uint8.
        Pixel values: 0 = non-road, 255 = road.

    Raises:
        ValueError: If image has fewer than 3 channels.
        RuntimeError: If model inference fails.

    Note:
        Requirement: REQ-AI-001 (Road Extraction)
        Decision: DEC-XXXX (Model Selection)
    """
```

### Imports
```python
# Standard library
import os
from pathlib import Path

# Third-party
import numpy as np
import torch
from PIL import Image

# Project
from ai.models import RoadExtractor
from gis.utils import apply_crs_transform
```

### Testing
```python
# Test files mirror source structure
# ai/models/road_extractor.py → tests/unit/ai/models/test_road_extractor.py

class TestRoadExtractor:
    """Tests for RoadExtractor class."""

    def test_extract_roads_returns_binary_mask(self):
        """Verify output is a binary mask with correct dimensions."""
        ...

    def test_extract_roads_handles_occluded_input(self):
        """Verify model handles partially occluded images gracefully."""
        ...
```

---

## JavaScript/TypeScript Standards

> To be defined during Phase 5 (Architecture) when frontend technology is selected.

---

## Configuration Standards

- Use YAML for configuration files where possible
- Environment-specific values go in `.env` files (never committed)
- Default values are documented in code
- Configuration is validated at application startup

---

## Version Control Standards

- See [Contributing Guidelines](../.github/CONTRIBUTING.md) for commit conventions and branch strategy
- Every commit message references a requirement, decision, or issue
- No commented-out code in committed files (use branches for experiments)

---

*Standards are updated as technology decisions are finalized.*
