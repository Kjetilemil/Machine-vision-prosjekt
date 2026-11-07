import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from processing.erase import erase_line


def test_erase_line_makes_the_line_white():
    image = np.zeros((20, 30, 3), dtype=np.uint8)

    erase_line(image, (5, 10), (25, 10), 3)

    assert np.all(image[10, 8:22] == 255)
    assert np.all(image[0] == 0)  # far away from the line nothing changes


def test_erase_line_on_one_point_erases_a_dot():
    image = np.zeros((20, 30, 3), dtype=np.uint8)

    erase_line(image, (15, 10), (15, 10), 5)

    assert np.all(image[10, 15] == 255)
