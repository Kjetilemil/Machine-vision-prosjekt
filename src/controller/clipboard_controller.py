from image.convert_image_for_gui import convert_opencv_to_gui_image
from image.copy import copy_image
from image.properties import get_image_properties
from image.blank_canvas import create_blank_canvas

# copies the current image or the selected area of the image to the clipboard
def run_copy_image(controller):
        if controller.current_img is None:
            return

        if controller.selection_type == "rectangle":
            controller.copied_image = copy_image(controller.get_selected_area())
            controller.window.display_status("Selected area copied.")
        else:
            controller.copied_image = copy_image(controller.current_img)
            controller.window.display_status("No selection made. Copying the entire image.")

# paste the copied image into the current image
def run_paste_image(controller):
        if controller.copied_image is None:
            return

        controller.history.save(controller.current_img)
        controller.current_img = copy_image(controller.copied_image)
        controller.current_path = None
        gui_image = convert_opencv_to_gui_image(controller.current_img)
        controller.window.display_image(gui_image)

# cuts the current image
def run_cut_image(controller):
        if controller.current_img is None:
            return

        controller.copy_image()  # Copy the current image or selected area to the clipboard
        controller.history.save(controller.current_img)

        if controller.selection_type == "rectangle":
            controller.current_img = copy_image(controller.current_img) # Copy the current image for undo purposes
            location = controller.get_selected_area()
            location[:] = 255  # Fill the selected area with white

        else:
            height, width, channels = get_image_properties(controller.current_img)
            controller.current_img = create_blank_canvas(width, height, (255, 255, 255))

        gui_image = convert_opencv_to_gui_image(controller.current_img)
        controller.window.display_image(gui_image)
        controller.window.display_status("Image cut")