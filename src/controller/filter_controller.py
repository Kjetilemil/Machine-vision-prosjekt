from image.convert_image_for_gui import convert_opencv_to_gui_image
from processing.binary import apply_binary_filter
from processing.constants import (
    DEFAULT_BINARY_THRESHOLD,
    DEFAULT_GAUSSIAN_KERNEL_SIZE,
    DEFAULT_SOBEL_KERNEL_SIZE,
)
from processing.histogram_thresholding import apply_histogram_thresholding
from processing.gaussian import apply_gaussian_filter
from processing.sobel import apply_sobel_filter

from gui.popup import popup_get_integer



def run_apply_gaussian_filter(controller):
        if controller.current_img is None:
            return

        kernel_size = popup_get_integer(10, 1, 501, "Enter kernel size between 1 and 501 (must be odd)", controller.window)
        
        if kernel_size is None:
            kernel_size = DEFAULT_GAUSSIAN_KERNEL_SIZE
        elif kernel_size % 2 == 0:
            kernel_size += 1
        
        processed_image = apply_gaussian_filter(
            controller.current_img,
            kernel_size=kernel_size,
        )
        controller.history.save(controller.current_img)
        controller.current_img = processed_image

        gui_image = convert_opencv_to_gui_image(processed_image)
        controller.window.display_image(gui_image)


def run_apply_sobel_filter(controller):
        if controller.current_img is None:
            return

        kernel_size = popup_get_integer(3, 1, 5, "Enter kernel size between 1 and 5", controller.window)
        
        if kernel_size is None:
            kernel_size = DEFAULT_SOBEL_KERNEL_SIZE

        processed_image = apply_sobel_filter(
            controller.current_img,
            kernel_size=kernel_size,
        )
        controller.history.save(controller.current_img)
        controller.current_img = processed_image

        gui_image = convert_opencv_to_gui_image(processed_image)
        controller.window.display_image(gui_image)

def run_apply_binary_filter(controller):
        if controller.current_img is None:
            return

        threshold = popup_get_integer(127, 0, 225, "Enter binary threshold between 0 and 255", controller.window)
                
        if threshold is None:
            threshold = DEFAULT_BINARY_THRESHOLD

        processed_image = apply_binary_filter(
            controller.current_img,
            threshold=threshold,
        )
        controller.history.save(controller.current_img)
        controller.current_img = processed_image

        gui_image = convert_opencv_to_gui_image(processed_image)
        controller.window.display_image(gui_image)


def run_apply_histogram_thresholding(controller):
        if controller.current_img is None:
            return

        processed_image = apply_histogram_thresholding(controller.current_img)
        controller.history.save(controller.current_img)
        controller.current_img = processed_image

        gui_image = convert_opencv_to_gui_image(processed_image)
        controller.window.display_image(gui_image)