import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from processing.brush import paint_line


def test_paint_line_paints_between_the_points():
    image = np.zeros((50, 50, 3), dtype=np.uint8)

    result = paint_line(image, (10, 25), (40, 25), (0, 0, 255), 5)

    assert np.array_equal(result[25, 25], (0, 0, 255))  # the middle of the line is red
    assert np.array_equal(result[5, 25], (0, 0, 0))     # far away from the line nothing changed


def test_paint_line_to_the_same_point_makes_a_dot():
    image = np.zeros((50, 50, 3), dtype=np.uint8)

    result = paint_line(image, (25, 25), (25, 25), (255, 255, 255), 9)

    assert np.array_equal(result[25, 25], (255, 255, 255))
    assert np.array_equal(result[25, 40], (0, 0, 0))
