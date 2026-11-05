import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from processing.object_effects import blur_object, recolor_object


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


def test_recolor_object_only_changes_the_object():
    image = np.zeros((20, 30, 3), dtype=np.uint8)
    image[:] = (0, 0, 255)  # red in BGR
    mask = make_mask()

    result = recolor_object(image, mask, (255, 0, 0))  # blue in BGR

    assert result.shape == image.shape
    assert result.dtype == image.dtype
    assert np.array_equal(result[:, 15:], image[:, 15:])
    blue, green, red = result[0, 0].astype(int)
    assert blue > red and blue > green


def test_recolor_object_keeps_light_and_shadow():
    image = np.zeros((20, 30, 3), dtype=np.uint8)
    image[:, :, 2] = np.linspace(50, 250, 30, dtype=np.uint8)  # red that goes from dark to bright
    mask = np.full((20, 30), 255, dtype=np.uint8)

    result = recolor_object(image, mask, (0, 255, 0))  # green in BGR

    # it is green now, but the dark side is still darker than the bright side
    blue, green, red = result[0, -1].astype(int)
    assert green > red and green > blue
    assert result[0, 0, 1] < result[0, -1, 1]
