import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from processing.polygon_selection import polygon_mask, draw_selection_line, is_close_to


def test_polygon_mask_fills_inside_the_points():
    image = np.zeros((100, 100, 3), dtype=np.uint8)
    triangle = [(10, 10), (90, 10), (50, 90)]

    mask = polygon_mask(image, triangle)

    assert mask.shape == (100, 100)
    assert mask[30, 50] == 255  # inside the triangle
    assert mask[90, 10] == 0    # outside the triangle


def test_draw_selection_line_does_not_change_the_image():
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    preview = draw_selection_line(image, [(10, 10), (90, 10), (90, 90)])

    assert not image.any()  # the original is still black
    assert preview.any()    # the copy has the yellow line


def test_is_close_to():
    image = np.zeros((600, 600, 3), dtype=np.uint8)

    assert is_close_to((100, 100), (105, 103), image)
    assert not is_close_to((100, 100), (300, 300), image)