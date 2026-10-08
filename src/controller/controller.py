from controller.file_controller import open_image, save_image, save_image_as
from image.convert_image_for_gui import convert_opencv_to_gui_image
from processing.binary import apply_binary_filter
from processing.constants import (
    DEFAULT_BINARY_THRESHOLD,
    DEFAULT_GAUSSIAN_KERNEL_SIZE,
    DEFAULT_SOBEL_KERNEL_SIZE,
)
from processing.gaussian import apply_gaussian_filter
from processing.sobel import apply_sobel_filter


class Controller:
    def __init__(self, window):
        self.window = window
        self.current_img = None
        self.current_path = None

    def open_image(self):
        open_image(self)

    def save_image(self):
        save_image(self)

    def save_image_as(self):
        save_image_as(self)

    def apply_gaussian_filter(self):
        if self.current_img is None:
            return

        processed_image = apply_gaussian_filter(
            self.current_img,
            kernel_size=DEFAULT_GAUSSIAN_KERNEL_SIZE,
        )
        self.current_img = processed_image

        gui_image = convert_opencv_to_gui_image(processed_image)
        self.window.display_image(gui_image)

    def apply_sobel_filter(self):
        if self.current_img is None:
            return

        processed_image = apply_sobel_filter(
            self.current_img,
            kernel_size=DEFAULT_SOBEL_KERNEL_SIZE,
        )
        self.current_img = processed_image

        gui_image = convert_opencv_to_gui_image(processed_image)
        self.window.display_image(gui_image)

    def apply_binary_filter(self):
        if self.current_img is None:
            return

        processed_image = apply_binary_filter(
            self.current_img,
            threshold=DEFAULT_BINARY_THRESHOLD,
        )
        self.current_img = processed_image

        gui_image = convert_opencv_to_gui_image(processed_image)
        self.window.display_image(gui_image)
