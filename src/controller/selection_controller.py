import time

from image.convert_image_for_gui import convert_opencv_to_gui_image
from processing.object_selection import draw_selection
from processing.polygon_selection import polygon_mask, draw_selection_line, is_close_to


# ---------- free-form: hold the mouse button and draw around the area ----------

def run_select_freeform_tool(controller):
    controller.current_tool = "freeform_selection"
    controller.selection_points = []
    controller.window.set_draw_mode(True)
    controller.window.display_status("Free-form selection: hold the mouse button and draw around the area.")


def run_start_freeform(controller, x, y):
    if controller.current_tool != "freeform_selection" or controller.current_img is None:
        return
    controller.selection_points = [(x, y)]


def run_move_freeform(controller, x, y):
    if controller.current_tool != "freeform_selection" or not controller.selection_points:
        return
    controller.selection_points.append((x, y))

    # redrawing a big image is slow, so the preview is only updated about 20 times per second
    now = time.monotonic()
    if now - getattr(controller, "last_preview_time", 0) < 0.05:
        return
    controller.last_preview_time = now

    preview = draw_selection_line(controller.current_img, controller.selection_points)
    controller.window.display_image(convert_opencv_to_gui_image(preview))


def run_finish_freeform(controller, x, y):
    if controller.current_tool != "freeform_selection" or not controller.selection_points:
        return
    controller.selection_points.append((x, y))
    _finish_selection(controller, "freeform")


# ---------- polygon: click the corners, click the first corner again to finish ----------

def run_select_polygon_tool(controller):
    controller.current_tool = "polygon_selection"
    controller.selection_points = []
    controller.window.set_draw_mode(False)
    controller.window.display_status("Polygon selection: click the corners, click the first corner again to finish.")


def run_polygon_click(controller, x, y):
    if controller.current_tool != "polygon_selection" or controller.current_img is None:
        return

    points = controller.selection_points
    # clicking the first corner again closes the polygon
    if len(points) >= 3 and is_close_to((x, y), points[0], controller.current_img):
        _finish_selection(controller, "polygon")
        return

    points.append((x, y))
    preview = draw_selection_line(controller.current_img, points)
    controller.window.display_image(convert_opencv_to_gui_image(preview))
    controller.window.display_status(f"Polygon selection: {len(points)} corners. Click the first corner to finish.")


# ---------- the last step is the same for both tools ----------

def _finish_selection(controller, selection_type):
    points = controller.selection_points
    controller.selection_points = []

    if len(points) < 3:
        controller.window.display_image(convert_opencv_to_gui_image(controller.current_img))
        controller.window.display_status("The selection needs at least 3 points, try again.")
        return

    mask = polygon_mask(controller.current_img, points)
    if not mask.any():
        controller.window.display_image(convert_opencv_to_gui_image(controller.current_img))
        controller.window.display_status("The selection is empty, try again.")
        return

    # the same mask as Select object, so remove, blur and change color work on it
    controller.selected_mask = mask
    controller.selection_type = selection_type
    preview = draw_selection(controller.current_img, mask)
    controller.window.display_image(convert_opencv_to_gui_image(preview))
    pixels = int((mask > 0).sum())
    controller.window.display_status(f"Area selected ({pixels} pixels)")