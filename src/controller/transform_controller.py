from image.convert_image_for_gui import convert_opencv_to_gui_image
from processing.rotate_flip import rotate_right, rotate_left, flip_horizontal, flip_vertical
from processing.resize import resize_image 
from processing.crop import crop_to_mask



def run_rotate_right(controller):
        if controller.current_img is None:
            return
    
        processed_image = rotate_right(controller.current_img)
        controller.history.save(controller.current_img)
        controller.current_img = processed_image
    
        gui_image = convert_opencv_to_gui_image(processed_image)
        controller.window.display_image(gui_image)


def run_rotate_left(controller):
        if controller.current_img is None:
            return
    
        processed_image = rotate_left(controller.current_img)
        controller.history.save(controller.current_img)
        controller.current_img = processed_image
    
        gui_image = convert_opencv_to_gui_image(processed_image)
        controller.window.display_image(gui_image)

def run_flip_horizontal(controller):
        if controller.current_img is None:
            return
    
        processed_image = flip_horizontal(controller.current_img)
        controller.history.save(controller.current_img)
        controller.current_img = processed_image
    
        gui_image = convert_opencv_to_gui_image(processed_image)
        controller.window.display_image(gui_image)

def run_flip_vertical(controller):
        if controller.current_img is None:
            return
    
        processed_image = flip_vertical(controller.current_img)
        controller.history.save(controller.current_img)
        controller.current_img = processed_image
    
        gui_image = convert_opencv_to_gui_image(processed_image)
        controller.window.display_image(gui_image)

# Resize the current image to new dimensions provided by the user
def run_resize_image(controller):
        if controller.current_img is None:
            return

        width, height = controller.window.ask_for_resize_dimensions()
        if width is None or height is None:
            return

        resized_image = resize_image(controller.current_img, width, height)
        controller.history.save(controller.current_img)
        controller.current_img = resized_image

        gui_image = convert_opencv_to_gui_image(resized_image)
        controller.window.display_image(gui_image)

# crops the image to the selected area. works with every selection (rectangle, free-form, polygon, object)
def run_crop_image(controller):
        mask = controller.selected_mask
        if controller.current_img is None or mask is None or not mask.any():
            controller.window.display_status("Select an area first.")
            return
        # the image may have been rotated or resized since the area was selected
        if mask.shape != controller.current_img.shape[:2]:
            controller.selected_mask = None
            controller.window.display_status("The image has changed, select the area again.")
            return

        controller.history.save(controller.current_img)
        controller.current_img = crop_to_mask(controller.current_img, mask)
        # the selection does not fit the cropped image any more
        controller.selected_mask = None
        controller.rectangle = None
        controller.selection_type = None
        gui_image = convert_opencv_to_gui_image(controller.current_img)
        controller.window.display_image(gui_image)
