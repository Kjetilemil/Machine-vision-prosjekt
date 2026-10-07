import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from processing.gaussian import apply_gaussian_filter


def test_gaussian_filter_preserves_shape_and_type():
    image = np.zeros((20, 30, 3), dtype=np.uint8)
    result = apply_gaussian_filter(image)

    assert result.shape == image.shape
    assert result.dtype == image.dtype
