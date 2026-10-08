import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from processing.binary import apply_binary_filter


def test_binary_filter_preserves_shape_and_type():
    image = np.zeros((20, 30, 3), dtype=np.uint8)
    result = apply_binary_filter(image, threshold=127)

    assert result.shape == image.shape
    assert result.dtype == np.uint8
