import numpy as np

from image.convert_image_for_gui import convert_opencv_to_gui_image
from processing.clipboard import (
    copy_area, cut_area, paste_area, selection_position,
    keep_piece_on_image, is_on_piece, draw_paste_frame,
)

# returns the mask of the current selection (rectangle, free-form, polygon or object), or None if nothing is selected
def _selection_mask(controller):
        mask = controller.selected_mask
        if mask is None or not mask.any():
            return None
        # the image may have been rotated or resized since the area was selected
        if mask.shape != controller.current_img.shape[:2]:
            return None
        return mask

# copies the selected area to the clipboard, or the entire image if nothing is selected
def run_copy_image(controller):
        if controller.current_img is None:
            return

        mask = _selection_mask(controller)
        if mask is None:
            mask = np.full(controller.current_img.shape[:2], 255, dtype=np.uint8)
            controller.window.display_status("No selection made. Copying the entire image.")
        else:
            controller.window.display_status("Selected area copied.")

        controller.copied_image, controller.copied_mask = copy_area(controller.current_img, mask)

# pastes the copied area into the selected area, or into the top left corner if nothing is selected.
# the piece is in the image right away, but it can be moved by dragging until it is placed with Enter
def run_paste_image(controller):
        if controller.copied_image is None or controller.current_img is None:
            return

        mask = _selection_mask(controller)
        position = (0, 0) if mask is None else selection_position(mask)

        # the whole paste, with all moves, is one undo step
        controller.history.save(controller.current_img)
        controller.floating_paste = {
            "base": controller.current_img,  # the image before the paste, the piece is moved on top of it
            "piece": controller.copied_image,
            "mask": controller.copied_mask,
        }
        _place_paste(controller, position)
        controller.current_tool = "move_paste"
        controller.window.set_draw_mode(True)
        controller.window.display_status("Pasted. Drag to move it, Enter to place it, Esc to cancel.")

def run_start_paste_drag(controller, x, y):
        if not _can_move_paste(controller):
            return

        paste = controller.floating_paste
        # a click next to the piece places it, like in Paint
        if not is_on_piece(paste["piece"], paste["position"], (x, y)):
            run_finish_paste(controller)
            return
        # remember where on the piece the mouse grabbed it, so the piece does not jump
        controller.paste_grab = (x - paste["position"][0], y - paste["position"][1])

# shows the piece at the new place while dragging, the image is only changed when the mouse is released
def run_move_paste_drag(controller, x, y):
        if controller.paste_grab is None:
            return

        paste = controller.floating_paste
        position = _drag_position(controller, x, y)
        preview = paste_area(paste["base"], paste["piece"], paste["mask"], position)
        preview = draw_paste_frame(preview, paste["piece"], position)
        controller.window.display_image(convert_opencv_to_gui_image(preview))

def run_finish_paste_drag(controller, x, y):
        if controller.paste_grab is None:
            return

        _place_paste(controller, _drag_position(controller, x, y))
        controller.paste_grab = None

# places the pasted piece for good (Enter, or a click next to the piece)
def run_finish_paste(controller):
        if not _can_move_paste(controller):
            return

        controller.floating_paste = None
        controller.paste_grab = None
        controller.current_tool = None
        controller.window.set_draw_mode(False)
        controller.window.display_image(convert_opencv_to_gui_image(controller.current_img))
        controller.window.display_status("Pasted image placed.")

# takes the paste back (Esc), Redo brings it back. returns False if there was no paste to take back
def run_cancel_paste(controller):
        if not _can_move_paste(controller):
            return False

        controller.current_img = controller.history.undo(controller.current_img)
        controller.floating_paste = None
        controller.paste_grab = None
        controller.current_tool = None
        controller.window.set_draw_mode(False)
        controller.window.display_image(convert_opencv_to_gui_image(controller.current_img))
        controller.window.display_status("Paste cancelled.")
        return True

# the piece can be moved as long as the paste tool is used and nothing else has changed the image
def _can_move_paste(controller):
        paste = controller.floating_paste
        return (
            paste is not None
            and controller.current_tool == "move_paste"
            and controller.current_img is paste["image"]
        )

def _drag_position(controller, x, y):
        paste = controller.floating_paste
        grab_x, grab_y = controller.paste_grab
        return keep_piece_on_image(paste["base"], paste["piece"], (x - grab_x, y - grab_y))

# puts the piece on the image from before the paste at the position, and shows it with a frame
def _place_paste(controller, position):
        paste = controller.floating_paste
        controller.current_img = paste_area(paste["base"], paste["piece"], paste["mask"], position)
        paste["position"] = position
        paste["image"] = controller.current_img
        preview = draw_paste_frame(controller.current_img, paste["piece"], position)
        controller.window.display_image(convert_opencv_to_gui_image(preview))

# cuts the selected area, or the entire image if nothing is selected
def run_cut_image(controller):
        if controller.current_img is None:
            return

        controller.copy_image()  # Copy the current image or selected area to the clipboard
        mask = _selection_mask(controller)
        if mask is None:
            mask = np.full(controller.current_img.shape[:2], 255, dtype=np.uint8)

        controller.history.save(controller.current_img)
        controller.current_img = cut_area(controller.current_img, mask)

        gui_image = convert_opencv_to_gui_image(controller.current_img)
        controller.window.display_image(gui_image)
        controller.window.display_status("Image cut")
