from image.convert_image_for_gui import convert_opencv_to_gui_image
from processing.rotate_flip import rotate_right, rotate_left, flip_horizontal, flip_vertical
from processing.resize import resize_image 
from processing.crop import crop



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

# crops the image. uses the rectangle defined by the rectangle selection tool
def run_crop_image(controller):
        if controller.current_img is None or controller.rectangle is None:
            controller.window.display_status("Select an area with the rectangle tool first.")
            return

        # corners from the rectangle selection tool
        top_left, bottom_right = controller.rectangle
        x0, y0 = top_left
        x1, y1 = bottom_right

        controller.history.save(controller.current_img)
        controller.current_img = crop(controller.current_img, x0, x1, y0, y1)
        controller.rectangle = None  # Reset the rectangle after cropping
        controller.selection_type = None  # Reset selection type after cropping
        gui_image = convert_opencv_to_gui_image(controller.current_img)
        controller.window.display_image(gui_image)
