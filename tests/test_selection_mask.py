import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from processing.crop import crop_to_mask


def make_image():
    # every pixel has its own value, so we can see where a pixel came from
    image = np.arange(20 * 30 * 3, dtype=np.uint32).reshape(20, 30, 3) % 250
    return image.astype(np.uint8)


def make_triangle_mask():
    # a triangle inside the box x 5-14, y 2-11
    mask = np.zeros((20, 30), dtype=np.uint8)
    for row in range(10):
        mask[2 + row, 5:5 + row + 1] = 255
    return mask


def test_crop_to_mask_keeps_the_box_around_the_selection():
    image = make_image()

    result = crop_to_mask(image, make_triangle_mask())

    assert np.array_equal(result, image[2:12, 5:15])


class Window:
    def set_draw_mode(self, enabled):
        self.draw_mode = enabled

    def cancel_zoom_preview(self):
        pass

    def display_image(self, image):
        self.shown = image

    def display_status(self, text):
        self.status = text


def make_controller(monkeypatch):
    from controller import clipboard_controller, tool_controller, transform_controller, object_controller
    from controller.controller import Controller

    # skip the conversion to a Qt image, it needs a running Qt app
    for module in (clipboard_controller, tool_controller, transform_controller, object_controller):
        monkeypatch.setattr(module, "convert_opencv_to_gui_image", lambda image: image)
    controller = Controller(Window())
    controller.current_img = make_image()
    return controller


def select_rectangle(controller, first, second):
    controller.select_rectangle_tool()
    controller.handle_image_click(*first)
    controller.handle_image_click(*second)


def click_object(controller, monkeypatch, mask):
    from controller import tool_controller

    # the real object detection needs a real photo, here we decide what it finds
    monkeypatch.setattr(tool_controller, "select_object", lambda image, x, y: mask)
    controller.select_object_tool()
    controller.handle_image_click(7, 9)


def test_rectangle_selection_works_with_blur(monkeypatch):
    controller = make_controller(monkeypatch)
    image_before = controller.current_img.copy()

    select_rectangle(controller, (5, 2), (15, 8))
    controller.blur_selected_object()

    changed = np.any(controller.current_img != image_before, axis=2)
    assert changed[2:8, 5:15].any()
    assert not changed[10:, :].any()  # nothing outside the rectangle is changed


def test_rectangle_replaces_an_old_object_selection(monkeypatch):
    controller = make_controller(monkeypatch)
    old_object = np.zeros((20, 30), dtype=np.uint8)
    old_object[15:19, 20:28] = 255
    click_object(controller, monkeypatch, old_object)

    select_rectangle(controller, (5, 2), (15, 8))

    assert controller.selected_mask[5, 10] == 255
    assert controller.selected_mask[16, 22] == 0  # the old object is no longer selected


def test_copy_of_a_clicked_object_copies_only_the_object(monkeypatch):
    controller = make_controller(monkeypatch)
    mask = make_triangle_mask()
    click_object(controller, monkeypatch, mask)

    controller.copy_image()

    assert np.array_equal(controller.copied_image, controller.current_img[2:12, 5:15])
    assert np.array_equal(controller.copied_mask, mask[2:12, 5:15])


def test_object_selection_replaces_an_old_rectangle(monkeypatch):
    controller = make_controller(monkeypatch)
    select_rectangle(controller, (0, 0), (30, 20))

    click_object(controller, monkeypatch, make_triangle_mask())
    controller.copy_image()

    assert controller.copied_image.shape == (10, 10, 3)  # the triangle, not the old rectangle


def test_crop_with_an_object_selection(monkeypatch):
    controller = make_controller(monkeypatch)
    image_before = controller.current_img
    click_object(controller, monkeypatch, make_triangle_mask())

    controller.crop_image()

    assert np.array_equal(controller.current_img, image_before[2:12, 5:15])
    assert controller.selected_mask is None


def test_crop_with_a_rectangle_selection(monkeypatch):
    controller = make_controller(monkeypatch)
    image_before = controller.current_img

    select_rectangle(controller, (15, 8), (5, 2))  # the corners can be clicked in any order
    controller.crop_image()

    assert np.array_equal(controller.current_img, image_before[2:8, 5:15])


def test_empty_rectangle_is_no_selection(monkeypatch):
    controller = make_controller(monkeypatch)
    image_before = controller.current_img

    select_rectangle(controller, (5, 5), (5, 9))
    controller.remove_selected_object()

    assert controller.selected_mask is None
    assert controller.current_img is image_before
    assert controller.history.undo_stack == []  # no empty undo step


def test_crop_without_selection_does_nothing(monkeypatch):
    controller = make_controller(monkeypatch)
    image_before = controller.current_img

    controller.crop_image()

    assert controller.current_img is image_before
