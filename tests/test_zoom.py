import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from controller.controller import Controller
from gui.zoomable_label import ZoomableLabel
from processing.zoom import MAX_ZOOM, MIN_ZOOM, zoom_in, zoom_out


def test_zoom_in_and_out_change_zoom_by_one_step():
    assert zoom_in(1.0) == 1.25
    assert zoom_out(1.0) == 0.8


def test_zoom_stays_within_supported_limits():
    assert zoom_in(MAX_ZOOM) == MAX_ZOOM
    assert zoom_out(MIN_ZOOM) == MIN_ZOOM


def test_controller_waits_for_selected_zoom_location():
    class Window:
        def start_zoom_preview(self, zoom_factor, callback):
            self.preview = (zoom_factor, callback)

        def set_zoom_factor(self, *args):
            self.zoom = args

    window = Window()
    image = object()
    controller = Controller(window)
    controller.current_img = image

    controller.zoom_in()

    assert window.preview[0] == 1.25
    assert controller.zoom_factor == 1.0
    assert not hasattr(window, "zoom")

    window.preview[1](0.3, 0.7, 0.4, 0.6)

    assert controller.zoom_factor == 1.25
    assert window.zoom == (1.25, 0.3, 0.7, 0.4, 0.6)
    assert controller.current_img is image


def test_controller_zoom_out_applies_immediately_without_location_selection():
    class Window:
        def __init__(self):
            self.zoom_factors = []

        def set_zoom_factor(self, zoom_factor):
            self.zoom_factors.append(zoom_factor)

        def start_zoom_preview(self, *args):
            raise AssertionError("Zoom out should not start a selection preview")

    window = Window()
    controller = Controller(window)
    controller.current_img = object()

    controller.zoom_out()

    assert controller.zoom_factor == 0.8
    assert window.zoom_factors == [0.8]


def test_zoomed_image_is_centered_when_it_fits_in_view():
    offset = ZoomableLabel._image_offset(100, 80, 90, 0.9)

    assert offset == 10


def test_oversized_image_stays_inside_viewport_while_using_focus():
    left_offset = ZoomableLabel._image_offset(100, 150, 0, 0)
    right_offset = ZoomableLabel._image_offset(100, 150, 100, 1)

    assert left_offset == 0
    assert right_offset == -50