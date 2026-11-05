import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from processing.object_selection import remove_object


def make_image_and_mask():
    # a big gray image with a black square in the middle
    image = np.full((200, 3000, 3), 128, dtype=np.uint8)
    image[50:150, 1400:1600] = 0

    # the mask is 5 pixels too small on every side, like a rough mask from the small copy
    mask = np.zeros((200, 3000), dtype=np.uint8)
    mask[55:145, 1405:1595] = 255
    return image, mask


def test_remove_object_removes_edges_on_big_image():
    image, mask = make_image_and_mask()

    result = remove_object(image, mask)

    # no dark pixels from the square should be left
    assert result[50:150, 1400:1600].min() > 100


def test_remove_object_adds_texture_like_the_surroundings():
    # a noisy "skin" image with a black square in the middle
    image = np.random.default_rng(0).normal(128, 10, (200, 200, 3)).clip(0, 255).astype(np.uint8)
    image[80:120, 80:120] = 0
    mask = np.zeros((200, 200), dtype=np.uint8)
    mask[80:120, 80:120] = 255

    result = remove_object(image, mask)

    # the hole should not be smooth, it should be noisy like the rest of the image
    assert result[90:110, 90:110].std() > 3


def test_remove_object_keeps_the_rest_of_the_image():
    image, mask = make_image_and_mask()

    result = remove_object(image, mask)

    assert result.shape == image.shape
    assert result.dtype == image.dtype
    assert np.array_equal(result[:, :1300], image[:, :1300])
    assert np.array_equal(result[:, 1700:], image[:, 1700:])
