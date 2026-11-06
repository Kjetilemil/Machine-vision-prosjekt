from image.convert_image_for_gui import convert_opencv_to_gui_image
from gui.popup import popup_get_integer, popup_get_color, popup_get_text
from processing.object_selection import select_object, draw_selection, remove_object
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
