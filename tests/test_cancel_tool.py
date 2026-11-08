import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from controller import tool_controller
from controller.controller import Controller


class Window:
    def __init__(self):
        self.draw_mode = None
        self.shown = None

    def set_draw_mode(self, enabled):
        self.draw_mode = enabled

    def cancel_zoom_preview(self):
        pass

    def display_image(self, image):
        self.shown = image

    def display_status(self, text):
        self.status = text


def make_controller(monkeypatch):
    # skip the conversion to a Qt image, it needs a running Qt app
    monkeypatch.setattr(tool_controller, "convert_opencv_to_gui_image", lambda image: image)
    controller = Controller(Window())
    controller.current_img = np.zeros((20, 30, 3), dtype=np.uint8)
    return controller


def test_escape_leaves_the_tool_and_the_selection(monkeypatch):
    controller = make_controller(monkeypatch)
    controller.current_tool = "select_object"
    controller.selected_mask = np.full((20, 30), 255, dtype=np.uint8)
    controller.selection_points = [(1, 1)]
    controller.rectangle_corners = (2, 2)

    controller.cancel_tool()

    assert controller.current_tool is None
    assert controller.selected_mask is None
    assert controller.selection_points == []
    assert controller.rectangle_corners is None
    assert controller.window.draw_mode is False
    assert controller.window.shown is controller.current_img  # the selection is no longer drawn


def test_escape_during_a_move_only_stops_the_move(monkeypatch):
    controller = make_controller(monkeypatch)
    controller.current_tool = "move_object"
    controller.selected_mask = np.full((20, 30), 255, dtype=np.uint8)
    controller.move_start = (5, 5)

    controller.cancel_tool()

    assert controller.move_start is None
    assert controller.current_tool == "move_object"
    assert controller.selected_mask is not None
