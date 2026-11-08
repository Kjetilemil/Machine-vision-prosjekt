import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from processing.object_selection import remove_object, place_object, shift_image


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


def make_square_scene():
    # a gray background with a white square, and a mask that covers the square
    image = np.full((100, 100, 3), 128, dtype=np.uint8)
    image[20:50, 20:50] = 255
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[20:50, 20:50] = 255
    return image, mask


def test_shift_image_moves_the_mask():
    _, mask = make_square_scene()

    moved = shift_image(mask, (30, 10))

    assert moved[40, 65] == 255  # inside the square at the new place
    assert moved[25, 25] == 0    # the old place is empty


def test_place_object_puts_the_object_at_the_new_place():
    image, mask = make_square_scene()
    background = np.full((100, 100, 3), 128, dtype=np.uint8)

    result = place_object(background, image, mask, (40, 40))

    assert result.shape == image.shape
    assert result.dtype == image.dtype
    assert np.array_equal(result[75, 75], (255, 255, 255))  # the middle of the object
    assert np.array_equal(result[35, 35], (128, 128, 128))  # the old place is background
    assert np.array_equal(result[5, 5], (128, 128, 128))    # the rest is not changed


def test_place_object_can_go_partly_outside_the_image():
    image, mask = make_square_scene()
    background = np.full((100, 100, 3), 128, dtype=np.uint8)

    result = place_object(background, image, mask, (70, 0))

    assert result.shape == image.shape
    assert np.array_equal(result[35, 97], (255, 255, 255))
