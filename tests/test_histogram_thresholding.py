import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from processing.histogram_thresholding import apply_histogram_thresholding


def test_histogram_thresholding_preserves_shape_and_type():
    image = np.zeros((20, 30, 3), dtype=np.uint8)
    result = apply_histogram_thresholding(image)

    assert result.shape == image.shape
    assert result.dtype == np.uint8
