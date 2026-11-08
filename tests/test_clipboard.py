import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from processing.clipboard import (
    rectangle_mask, copy_area, cut_area, paste_area, selection_position,
    keep_piece_on_image, is_on_piece, draw_paste_frame,
)


def make_image():
    # every pixel has its own value, so we can see where a pixel came from
    image = np.arange(20 * 30 * 3, dtype=np.uint32).reshape(20, 30, 3) % 250
    return image.astype(np.uint8)


def make_triangle_mask():
    # a triangle (like a polygon selection) inside the box x 5-14, y 2-11
    mask = np.zeros((20, 30), dtype=np.uint8)
    for row in range(10):
        mask[2 + row, 5:5 + row + 1] = 255
    return mask


def test_rectangle_mask():
    image = make_image()

    mask = rectangle_mask(image, (5, 2), (15, 8))

    assert mask.shape == image.shape[:2]
    assert int((mask > 0).sum()) == 10 * 6
    assert mask[2, 5] == 255 and mask[8, 15] == 0


def test_copy_area_cuts_out_the_box_around_the_selection():
    image = make_image()
    mask = make_triangle_mask()

    piece, piece_mask = copy_area(image, mask)

    assert piece.shape == (10, 10, 3)
    assert np.array_equal(piece, image[2:12, 5:15])
    assert np.array_equal(piece_mask, mask[2:12, 5:15])


def test_cut_area_only_makes_the_selection_white():
    image = make_image()
    mask = make_triangle_mask()

    result = cut_area(image, mask)

    assert np.all(result[mask > 0] == 255)
    assert np.array_equal(result[mask == 0], image[mask == 0])
    assert not np.array_equal(image, result)  # the original image is not changed


def test_paste_area_only_pastes_the_selected_form():
    image = make_image()
    mask = make_triangle_mask()
    piece, piece_mask = copy_area(image, mask)
    target = np.zeros((20, 30, 3), dtype=np.uint8)

    result = paste_area(target, piece, piece_mask, (15, 5))

    pasted = result[5:15, 15:25]
    assert np.array_equal(pasted[piece_mask > 0], piece[piece_mask > 0])
    assert np.all(pasted[piece_mask == 0] == 0)  # the corners of the box around the triangle stay as they were
    assert np.all(result[:5] == 0)


def test_paste_area_leaves_out_what_does_not_fit():
    piece = np.full((10, 10, 3), 200, dtype=np.uint8)
    piece_mask = np.full((10, 10), 255, dtype=np.uint8)
    target = np.zeros((20, 30, 3), dtype=np.uint8)

    result = paste_area(target, piece, piece_mask, (25, 15))

    assert result.shape == target.shape
    assert np.all(result[15:, 25:] == 200)
    assert int((result == 200).all(axis=2).sum()) == 5 * 5


def test_paste_area_works_when_the_piece_is_moved_over_the_top_left_edge():
    piece = np.full((10, 10, 3), 200, dtype=np.uint8)
    piece_mask = np.full((10, 10), 255, dtype=np.uint8)
    target = np.zeros((20, 30, 3), dtype=np.uint8)

    result = paste_area(target, piece, piece_mask, (-6, -7))

    assert np.all(result[:3, :4] == 200)
    assert int((result == 200).all(axis=2).sum()) == 4 * 3


def test_keep_piece_on_image():
    image = np.zeros((20, 30, 3), dtype=np.uint8)
    piece = np.zeros((10, 10, 3), dtype=np.uint8)

    assert keep_piece_on_image(image, piece, (5, 5)) == (5, 5)
    assert keep_piece_on_image(image, piece, (-50, 100)) == (-9, 19)


def test_is_on_piece():
    piece = np.zeros((10, 10, 3), dtype=np.uint8)

    assert is_on_piece(piece, (5, 5), (5, 5))
    assert is_on_piece(piece, (5, 5), (14, 14))
    assert not is_on_piece(piece, (5, 5), (15, 5))


def test_draw_paste_frame_does_not_change_the_image():
    image = np.zeros((20, 30, 3), dtype=np.uint8)
    piece = np.zeros((10, 10, 3), dtype=np.uint8)

    preview = draw_paste_frame(image, piece, (5, 5))

    assert np.all(image == 0)
    assert not np.array_equal(preview, image)


def test_selection_position():
    assert selection_position(make_triangle_mask()) == (5, 2)
