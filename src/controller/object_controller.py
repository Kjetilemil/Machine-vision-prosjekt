from image.convert_image_for_gui import convert_opencv_to_gui_image
from gui.popup import popup_get_integer, popup_get_color, popup_get_text
from processing.object_selection import select_object, draw_selection, remove_object, place_object, shift_image
from processing.object_effects import blur_object, recolor_object


# removes the selected object and fills the gap with background
def run_remove_selected_object(controller):
        if controller.current_img is None or controller.selected_mask is None:
            controller.window.display_status("Select an object first.")
            return
        # the image may have been rotated or resized since the object was selected
        if controller.selected_mask.shape != controller.current_img.shape[:2]:
            controller.selected_mask = None
            controller.window.display_status("The image has changed, select the object again.")
            return

        controller.history.save(controller.current_img)
        controller.current_img = remove_object(controller.current_img, controller.selected_mask)
        controller.selected_mask = None
        controller.window.display_image(convert_opencv_to_gui_image(controller.current_img))
        controller.window.display_status("Object removed.")


# blurs the selected object
def run_blur_selected_object(controller):
        if controller.current_img is None or controller.selected_mask is None:
            controller.window.display_status("Select an object first.")
            return
        if controller.selected_mask.shape != controller.current_img.shape[:2]:
            controller.selected_mask = None
            controller.window.display_status("The image has changed, select the object again.")
            return

        controller.history.save(controller.current_img)
        controller.current_img = blur_object(controller.current_img, controller.selected_mask)
        controller.window.display_image(convert_opencv_to_gui_image(controller.current_img))
        controller.window.display_status("Object blurred.")


# asks for a color and gives it to the selected object
def run_recolor_selected_object(controller):
        if controller.current_img is None or controller.selected_mask is None:
            controller.window.display_status("Select an object first.")
            return
        if controller.selected_mask.shape != controller.current_img.shape[:2]:
            controller.selected_mask = None
            controller.window.display_status("The image has changed, select the object again.")
            return

        color = popup_get_color(controller.object_color, "Select object color", controller.window)
        if color is None:
            return
        controller.object_color = color

        controller.history.save(controller.current_img)
        bgr = (color.blue(), color.green(), color.red())
        controller.current_img = recolor_object(controller.current_img, controller.selected_mask, bgr)
        controller.window.display_image(convert_opencv_to_gui_image(controller.current_img))
        controller.window.display_status("Object color changed.")


# checks that there is a selected object that still fits the image
def _has_selection(controller):
        if controller.current_img is None or controller.selected_mask is None or not controller.selected_mask.any():
            controller.window.display_status("Select an object first.")
            return False

        if controller.selected_mask.shape != controller.current_img.shape[:2]:
            controller.selected_mask = None
            controller.window.display_status("The image has changed, select the object again.")
            return False

        return True


# selects the move or duplicate tool, the object is moved by dragging on the image
def run_select_move_tool(controller, tool):
        if not _has_selection(controller):
            return

        controller.current_tool = tool
        controller.window.set_draw_mode(True)
        controller.window.display_status("Drag on the image to place the object.")


def run_start_move(controller, x, y):
        if controller.current_tool not in ("move_object", "duplicate_object") or not _has_selection(controller):
            return

        controller.move_start = (x, y)
        # the background is only made once per drag, because filling the hole is slow
        if controller.current_tool == "move_object":
            controller.move_background = remove_object(controller.current_img, controller.selected_mask)
        else:
            controller.move_background = controller.current_img


# shows the object at the new place on a copy of the image, nothing is saved yet
def run_preview_move(controller, x, y):
        if controller.move_start is None:
            return

        offset = (x - controller.move_start[0], y - controller.move_start[1])
        preview = place_object(controller.move_background, controller.current_img, controller.selected_mask, offset)
        controller.window.display_image(convert_opencv_to_gui_image(preview))


def run_finish_move(controller, x, y):
        if controller.move_start is None:
            return

        offset = (x - controller.move_start[0], y - controller.move_start[1])
        background = controller.move_background
        controller.move_start = None
        controller.move_background = None

        # a click without dragging changes nothing
        if offset == (0, 0):
            controller.window.display_image(convert_opencv_to_gui_image(controller.current_img))
            return

        controller.history.save(controller.current_img)
        controller.current_img = place_object(background, controller.current_img, controller.selected_mask, offset)
        # the selection follows the object, so it can be moved again
        controller.selected_mask = shift_image(controller.selected_mask, offset)
        controller.window.display_image(convert_opencv_to_gui_image(controller.current_img))
        controller.window.display_status("Object placed. Drag again to move it more.")
