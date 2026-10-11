import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from controller import controller as controller_module
from controller.controller import Controller
from image.history import History, MAX_HISTORY


def test_undo_and_redo_go_back_and_forth():
    history = History()
    history.save("first")

    assert history.undo("second") == "first"
    assert history.redo("first") == "second"


def test_nothing_to_undo_or_redo_returns_none():
    history = History()

    assert history.undo("image") is None
    assert history.redo("image") is None


def test_new_change_removes_redo_steps():
    history = History()
    history.save("first")
    history.undo("second")

    history.save("first")

    assert history.redo("third") is None


def test_history_only_keeps_the_last_steps():
    history = History()
    for step in range(MAX_HISTORY + 5):
        history.save(step)

    assert len(history.undo_stack) == MAX_HISTORY
    assert history.undo_stack[0] == 5


def test_controller_undo_brings_back_the_image_before_rotate(monkeypatch):
    # skip the conversion to a Qt image, it needs a running Qt app
    monkeypatch.setattr(controller_module, "convert_opencv_to_gui_image", lambda image: image)

    class Window:
        def display_image(self, image):
            pass

        def display_status(self, text):
            self.status = text

    controller = Controller(Window())
    image = np.zeros((20, 30, 3), dtype=np.uint8)
    controller.current_img = image

    controller.rotate_right()
    assert controller.current_img.shape == (30, 20, 3)

    controller.undo()
    assert controller.current_img is image

    controller.redo()
    assert controller.current_img.shape == (30, 20, 3)
