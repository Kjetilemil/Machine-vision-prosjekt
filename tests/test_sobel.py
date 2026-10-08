import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from processing.sobel import apply_sobel_filter


def test_sobel_filter_returns_bgr_image_shape_and_type():
    image = np.zeros((20, 30, 3), dtype=np.uint8)
    result = apply_sobel_filter(image, kernel_size=3)

    assert result.shape == image.shape
    assert result.dtype == np.uint8
