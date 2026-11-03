import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from processing.shapes import SHAPES, draw_shape, constrain_end, is_too_small

FILL = (0, 0, 255)  # red in BGR
OUTLINE = (255, 0, 0)  # blue in BGR


@pytest.mark.parametrize("shape", SHAPES)
def test_draw_shape_draws_every_shape(shape):
    image = np.full((100, 100, 3), 255, dtype=np.uint8)

    result = draw_shape(image, shape, (10, 10), (90, 80), FILL, OUTLINE)

    assert result.shape == image.shape
    assert result.dtype == image.dtype
    assert not np.array_equal(result, image)
    assert np.all(image == 255)  # the original image is not changed


def test_draw_shape_uses_fill_and_outline_color():
    image = np.full((100, 100, 3), 255, dtype=np.uint8)

    result = draw_shape(image, "Rectangle", (10, 10), (90, 90), FILL, OUTLINE, thickness=3)

    assert tuple(result[50, 50]) == FILL
    assert tuple(result[10, 50]) == OUTLINE


def test_draw_shape_works_when_clicked_from_bottom_right():
    image = np.full((100, 100, 3), 255, dtype=np.uint8)

    result = draw_shape(image, "Rectangle", (90, 90), (10, 10), FILL, OUTLINE)

    assert tuple(result[50, 50]) == FILL


def test_constrain_end_keeps_proportions_with_shift():
    assert constrain_end("Rectangle", (10, 10), (90, 50)) == (90, 50)
    assert constrain_end("Rectangle", (10, 10), (90, 50), keep_proportions=True) == (50, 50)
    assert constrain_end("Ellipse", (50, 50), (10, 0), keep_proportions=True) == (10, 10)


def test_constrain_end_square_and_circle_always_have_equal_sides():
    assert constrain_end("Square", (10, 10), (90, 50)) == (50, 50)
    assert constrain_end("Circle", (10, 10), (30, 90)) == (30, 30)


def test_constrain_end_snaps_line_to_45_degrees():
    assert constrain_end("Line", (0, 0), (100, 5), keep_proportions=True) == (100, 0)
    end = constrain_end("Line", (0, 0), (100, 90), keep_proportions=True)
    assert end[0] == end[1]


def test_is_too_small():
    assert is_too_small("Rectangle", (10, 10), (11, 50))
    assert not is_too_small("Rectangle", (10, 10), (50, 50))
    assert not is_too_small("Line", (10, 10), (50, 10))


@pytest.mark.parametrize(
    "start, end, head",
    [
        ((10, 50), (90, 50), (75, 50)),  # right
        ((90, 50), (10, 50), (25, 50)),  # left
        ((50, 90), (50, 10), (50, 25)),  # up
        ((20, 20), (80, 80), (70, 70)),  # diagonal
    ],
)
def test_draw_shape_arrow_points_from_start_to_end(start, end, head):
    image = np.full((100, 100, 3), 255, dtype=np.uint8)

    result = draw_shape(image, "Arrow", start, end, FILL, OUTLINE)

    # the arrow head is close to the end point and the corner far away from the arrow stays white
    assert tuple(result[head[1], head[0]]) == FILL
    assert tuple(result[2, 97]) == (255, 255, 255)


def test_constrain_end_snaps_arrow_like_a_line():
    assert constrain_end("Arrow", (0, 0), (100, 5), keep_proportions=True) == (100, 0)
    assert constrain_end("Arrow", (0, 0), (100, 5)) == (100, 5)


def test_draw_shape_unknown_shape():
    image = np.full((100, 100, 3), 255, dtype=np.uint8)

    with pytest.raises(ValueError):
        draw_shape(image, "Banana", (10, 10), (90, 90), FILL, OUTLINE)
