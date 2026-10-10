from controller.file_controller import open_image, save_image, save_image_as, new_image
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
from image.properties import get_image_properties, get_pixel_color
from processing.resize import resize_image  
from processing.zoom import zoom_in as calculate_zoom_in, zoom_out as calculate_zoom_out
from image.copy import copy_image
from image.blank_canvas import create_blank_canvas 


class Controller:
    def __init__(self, window):
        self.window = window
        self.current_img = None
        self.current_path = None
        self.zoom_factor = 1.0
        self.current_tool = None 
        self.copied_image = None

    def zoom_in(self):
        self._start_zoom_preview(calculate_zoom_in)

    def zoom_out(self):
        if self.current_img is None:
            return

        self.zoom_factor = calculate_zoom_out(self.zoom_factor)
        self.window.set_zoom_factor(self.zoom_factor)

    def _start_zoom_preview(self, calculate_zoom):
        if self.current_img is None:
            return

        next_zoom = calculate_zoom(self.zoom_factor)
        self.window.start_zoom_preview(
            next_zoom,
            lambda image_x, image_y, view_x, view_y: self._apply_zoom(
                next_zoom, image_x, image_y, view_x, view_y
            ),
        )

    def _apply_zoom(self, zoom_factor, image_x, image_y, view_x, view_y):
        self.zoom_factor = zoom_factor
        self.window.set_zoom_factor(zoom_factor, image_x, image_y, view_x, view_y)

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

    # Resize the current image to new dimensions provided by the user
    def resize_image(self):
        if self.current_img is None:
            return

        width, height = self.window.ask_for_resize_dimensions()
        if width is None or height is None:
            return

        resized_image = resize_image(self.current_img, width, height)
        self.current_img = resized_image

        gui_image = convert_opencv_to_gui_image(resized_image)
        self.window.display_image(gui_image)
        

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

    def new_image(self):
        new_image(self)

    # selects the color picker tool
    def select_color_tool(self):
        self.current_tool = "color_picker"
        self.window.display_status("Color picker tool selected. Click on the image to pick a color.")

    def handle_image_click(self, x, y):
        if self.current_tool == "color_picker":
            if self.current_img is None:
                return

            blue, green, red = get_pixel_color(self.current_img, x, y)
            color_info = f"Color at ({x}, {y}): R={red}, G={green}, B={blue}"
            self.window.display_status(color_info)

    # copies the current image
    def copy_image(self):
        if self.current_img is None:
            return

        self.copied_image = copy_image(self.current_img)
        self.window.display_status("Image copied.")

    # paste the copied image into the current image
    def paste_image(self):
        if self.copied_image is None:
            return

        self.current_img = copy_image(self.copied_image)
        self.current_path = None
        gui_image = convert_opencv_to_gui_image(self.current_img)
        self.window.display_image(gui_image)

    # cuts the current image
    def cut_image(self):
        if self.current_img is None:
            return

        self.copied_image = copy_image(self.current_img)

        height, width, channels = get_image_properties(self.current_img)
        self.current_img = create_blank_canvas(width, height, (255, 255, 255))

        gui_image = convert_opencv_to_gui_image(self.current_img)
        self.window.display_image(gui_image)
        self.window.display_status("Image cut")
