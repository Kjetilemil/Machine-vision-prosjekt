from controller.file_controller import open_image, save_image, save_image_as
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
from processing.rotate_flip import rotate_right, rotate_left, flip_horizontal, flip_vertical
from image.properties import get_image_properties


class Controller:
    def __init__(self, window):
        self.window = window
        self.current_img = None
        self.current_path = None

    def open_image(self):
        open_image(self)

    def quit_application(self):
        self.window.close()

    def show_image_properties(self):
        if self.current_img is None:
            return None

        height, width, channels = get_image_properties(self.current_img)
        text = f"Height: {height}, Width: {width}, Channels: {channels}"
        self.window.display_text(text)
        

    def save_image(self):
        save_image(self)

    def save_image_as(self):
        save_image_as(self)

    def rotate_right(self):
        if self.current_img is None:
            return
    
        processed_image = rotate_right(self.current_img)
        self.current_img = processed_image
    
        gui_image = convert_opencv_to_gui_image(processed_image)
        self.window.display_image(gui_image)
    
    def rotate_left(self):
        if self.current_img is None:
            return
    
        processed_image = rotate_left(self.current_img)
        self.current_img = processed_image
    
        gui_image = convert_opencv_to_gui_image(processed_image)
        self.window.display_image(gui_image)
    
    def flip_horizontal(self):
        if self.current_img is None:
            return
    
        processed_image = flip_horizontal(self.current_img)
        self.current_img = processed_image
    
        gui_image = convert_opencv_to_gui_image(processed_image)
        self.window.display_image(gui_image)
    
    def flip_vertical(self):
        if self.current_img is None:
            return
    
        processed_image = flip_vertical(self.current_img)
        self.current_img = processed_image
    
        gui_image = convert_opencv_to_gui_image(processed_image)
        self.window.display_image(gui_image)
    
    

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

    def apply_histogram_thresholding(self):
        if self.current_img is None:
            return

        processed_image = apply_histogram_thresholding(self.current_img)
        self.current_img = processed_image

        gui_image = convert_opencv_to_gui_image(processed_image)
        self.window.display_image(gui_image)

    