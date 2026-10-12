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
from processing.zoom import zoom_by as calculate_zoom_by
from image.copy import copy_image
from image.blank_canvas import create_blank_canvas
from processing.object_selection import select_object, draw_selection, remove_object
from processing.object_effects import blur_object, shift_object_color
from image.history import History


class Controller:
    def __init__(self, window):
        self.window = window
        self.current_img = None
        self.current_path = None
        self.zoom_factor = 1.0
        self.current_tool = None 
        self.copied_image = None
        self.selected_mask = None
        self.history = History()

    # goes back to the image before the last change
    def undo(self):
        previous_image = self.history.undo(self.current_img)
        if previous_image is None:
            self.window.display_status("Nothing to undo.")
            return

        self.current_img = previous_image
        self.window.display_image(convert_opencv_to_gui_image(self.current_img))
        self.window.display_status("Undo.")

    # brings back the change that was undone
    def redo(self):
        next_image = self.history.redo(self.current_img)
        if next_image is None:
            self.window.display_status("Nothing to redo.")
            return

        self.current_img = next_image
        self.window.display_image(convert_opencv_to_gui_image(self.current_img))
        self.window.display_status("Redo.")

    def zoom_in(self):
        self._start_zoom_preview(calculate_zoom_in)

    # zooms in one step right away, used by the keyboard shortcut
    def zoom_in_directly(self):
        if self.current_img is None:
            return

        self.zoom_factor = calculate_zoom_in(self.zoom_factor)
        self.window.set_zoom_factor(self.zoom_factor)

    # zooms with pinch on the trackpad
    def zoom_by(self, factor):
        if self.current_img is None:
            return

        self.zoom_factor = calculate_zoom_by(self.zoom_factor, factor)
        self.window.set_zoom_factor(self.zoom_factor)

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
        self.history.save(self.current_img)
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
        self.history.save(self.current_img)
        self.current_img = processed_image
    
        gui_image = convert_opencv_to_gui_image(processed_image)
        self.window.display_image(gui_image)
    
    def rotate_left(self):
        if self.current_img is None:
            return
    
        processed_image = rotate_left(self.current_img)
        self.history.save(self.current_img)
        self.current_img = processed_image
    
        gui_image = convert_opencv_to_gui_image(processed_image)
        self.window.display_image(gui_image)
    
    def flip_horizontal(self):
        if self.current_img is None:
            return
    
        processed_image = flip_horizontal(self.current_img)
        self.history.save(self.current_img)
        self.current_img = processed_image
    
        gui_image = convert_opencv_to_gui_image(processed_image)
        self.window.display_image(gui_image)
    
    def flip_vertical(self):
        if self.current_img is None:
            return
    
        processed_image = flip_vertical(self.current_img)
        self.history.save(self.current_img)
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
        self.history.save(self.current_img)
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
        self.history.save(self.current_img)
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
        self.history.save(self.current_img)
        self.current_img = processed_image

        gui_image = convert_opencv_to_gui_image(processed_image)
        self.window.display_image(gui_image)

    def apply_histogram_thresholding(self):
        if self.current_img is None:
            return

        processed_image = apply_histogram_thresholding(self.current_img)
        self.history.save(self.current_img)
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

        elif self.current_tool == "select_object":
            if self.current_img is None:
                return
            mask = select_object(self.current_img, x, y)
            if not mask.any():
                self.window.display_status("Could not find an object there.")
                return
            self.selected_mask = mask
            pixels = int((mask > 0).sum())
            self.window.display_status(f"Object selected ({pixels} pixels)")
            preview = draw_selection(self.current_img, mask)
            self.window.display_image(convert_opencv_to_gui_image(preview))

    # selects the object selection tool
    def select_object_tool(self):
        self.current_tool = "select_object"
        self.window.display_status("Select object: click on an object in the image.")

        # removes the selected object and fills the gap with background
    def remove_selected_object(self):
        if self.current_img is None or self.selected_mask is None:
            self.window.display_status("Select an object first.")
            return
        # the image may have been rotated or resized since the object was selected
        if self.selected_mask.shape != self.current_img.shape[:2]:
            self.selected_mask = None
            self.window.display_status("The image has changed, select the object again.")
            return

        self.history.save(self.current_img)
        self.current_img = remove_object(self.current_img, self.selected_mask)
        self.selected_mask = None
        self.window.display_image(convert_opencv_to_gui_image(self.current_img))
        self.window.display_status("Object removed.")

    # blurs the selected object
    def blur_selected_object(self):
        if self.current_img is None or self.selected_mask is None:
            self.window.display_status("Select an object first.")
            return
        if self.selected_mask.shape != self.current_img.shape[:2]:
            self.selected_mask = None
            self.window.display_status("The image has changed, select the object again.")
            return

        self.history.save(self.current_img)
        self.current_img = blur_object(self.current_img, self.selected_mask)
        self.window.display_image(convert_opencv_to_gui_image(self.current_img))
        self.window.display_status("Object blurred.")

    # changes the color of the selected object
    def shift_selected_object_color(self):
        if self.current_img is None or self.selected_mask is None:
            self.window.display_status("Select an object first.")
            return
        if self.selected_mask.shape != self.current_img.shape[:2]:
            self.selected_mask = None
            self.window.display_status("The image has changed, select the object again.")
            return

        self.history.save(self.current_img)
        self.current_img = shift_object_color(self.current_img, self.selected_mask)
        self.window.display_image(convert_opencv_to_gui_image(self.current_img))
        self.window.display_status("Object color changed.")

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

        self.history.save(self.current_img)
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
        self.history.save(self.current_img)
        self.current_img = create_blank_canvas(width, height, (255, 255, 255))

        gui_image = convert_opencv_to_gui_image(self.current_img)
        self.window.display_image(gui_image)
        self.window.display_status("Image cut")
