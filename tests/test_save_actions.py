import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from controller import file_controller


def test_save_uses_current_path_without_opening_dialog(monkeypatch):
    image = object()
    controller = SimpleNamespace(
        window=object(),
        current_img=image,
        current_path="existing.png",
    )
    saved = []

    monkeypatch.setattr(
        file_controller,
        "filesystem_save_image",
        lambda path, current_image: saved.append((path, current_image)),
    )
    monkeypatch.setattr(
        file_controller.QFileDialog,
        "getSaveFileName",
        lambda *args: pytest.fail("Save should not open a file dialog"),
    )

    file_controller.save_image(controller)

    assert saved == [("existing.png", image)]


def test_save_without_current_path_uses_save_as_and_remembers_path(monkeypatch):
    image = object()
    controller = SimpleNamespace(window=object(), current_img=image, current_path=None)
    saved = []

    monkeypatch.setattr(
        file_controller.QFileDialog,
        "getSaveFileName",
        lambda *args: ("new.png", ""),
    )
    monkeypatch.setattr(
        file_controller,
        "filesystem_save_image",
        lambda path, current_image: saved.append((path, current_image)),
    )

    file_controller.save_image(controller)

    assert saved == [("new.png", image)]
    assert controller.current_path == "new.png"


def test_save_as_always_asks_for_path(monkeypatch):
    image = object()
    controller = SimpleNamespace(
        window=object(),
        current_img=image,
        current_path="existing.png",
    )
    saved = []

    monkeypatch.setattr(
        file_controller.QFileDialog,
        "getSaveFileName",
        lambda *args: ("copy.png", ""),
    )
    monkeypatch.setattr(
        file_controller,
        "filesystem_save_image",
        lambda path, current_image: saved.append((path, current_image)),
    )

    file_controller.save_image_as(controller)

    assert saved == [("copy.png", image)]
    assert controller.current_path == "copy.png"


def test_save_as_adds_extension_from_selected_filter(monkeypatch):
    image = object()
    controller = SimpleNamespace(window=object(), current_img=image, current_path=None)
    saved = []

    monkeypatch.setattr(
        file_controller.QFileDialog,
        "getSaveFileName",
        lambda *args: ("new-image", "JPEG image (*.jpg *.jpeg)"),
    )
    monkeypatch.setattr(
        file_controller,
        "filesystem_save_image",
        lambda path, current_image: saved.append((path, current_image)),
    )

    file_controller.save_image_as(controller)

    assert saved == [("new-image.jpg", image)]
    assert controller.current_path == "new-image.jpg"
