import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from processing.object_effects import blur_object, shift_object_color


def make_mask():
    # the "object" is the left half of the image
    mask = np.zeros((20, 30), dtype=np.uint8)
    mask[:, :15] = 255
    return mask


def test_blur_object_only_changes_the_object():
    image = np.zeros((20, 30, 3), dtype=np.uint8)
    image[::2] = 255  # white and black stripes, so blurring makes a difference
    mask = make_mask()

    result = blur_object(image, mask, kernel_size=5)

    assert result.shape == image.shape
    assert result.dtype == image.dtype
    assert np.array_equal(result[:, 15:], image[:, 15:])
    assert not np.array_equal(result[:, :15], image[:, :15])


def test_shift_object_color_only_changes_the_object():
    image = np.zeros((20, 30, 3), dtype=np.uint8)
    image[:] = (0, 0, 255)  # red in BGR
    mask = make_mask()

    result = shift_object_color(image, mask, hue_shift=60)

    assert result.shape == image.shape
    assert result.dtype == image.dtype
    assert np.array_equal(result[:, 15:], image[:, 15:])
    assert not np.array_equal(result[:, :15], image[:, :15])
