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
from processing.shapes import SHAPES, draw_shape, constrain_end, is_too_small
from image.history import History
from gui.popup import popup_get_integer, popup_get_color, popup_get_text
from PyQt6.QtGui import QColor
from processing.rectangle_selection import rectangle_selection
from processing.crop import crop
from processing.text import add_text
from processing.brush import paint_line

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
        self.tool_color = QColor("black")
        self.brush_size = 3
        self.brush_last = None # last point of the brush stroke that is being painted
        self.rectangle = None # Store the rectangle selection coordinates
        self.rectangle_corners = None # Store the rectangle corners for drawing
        self.shape_names = SHAPES
        self.selected_shape = None
        self.shape_start = None
        # different defaults so the fill and the outline can be told apart
        self.shape_fill_color = QColor("red")
        self.shape_outline_color = QColor("blue")

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

        kernel_size = popup_get_integer(10, 1, 501, "Enter kernel size between 1 and 501 (must be odd)", self.window)
        
        if kernel_size is None:
            kernel_size = DEFAULT_GAUSSIAN_KERNEL_SIZE
        elif kernel_size % 2 == 0:
            kernel_size += 1
        
        processed_image = apply_gaussian_filter(
            self.current_img,
            kernel_size=kernel_size,
        )
        self.history.save(self.current_img)
        self.current_img = processed_image

        gui_image = convert_opencv_to_gui_image(processed_image)
        self.window.display_image(gui_image)

    def apply_sobel_filter(self):
        if self.current_img is None:
            return

        kernel_size = popup_get_integer(3, 1, 5, "Enter kernel size between 1 and 5", self.window)
        
        if kernel_size is None:
            kernel_size = DEFAULT_SOBEL_KERNEL_SIZE

        processed_image = apply_sobel_filter(
            self.current_img,
            kernel_size=kernel_size,
        )
        self.history.save(self.current_img)
        self.current_img = processed_image

        gui_image = convert_opencv_to_gui_image(processed_image)
        self.window.display_image(gui_image)

    def apply_binary_filter(self):
        if self.current_img is None:
            return

        threshold = popup_get_integer(127, 0, 225, "Enter binary threshold between 0 and 255", self.window)
                
        if threshold is None:
            threshold = DEFAULT_BINARY_THRESHOLD

        processed_image = apply_binary_filter(
            self.current_img,
            threshold=threshold,
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
        self.window.set_draw_mode(False)
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

        # rectangle selection tool. User clicks two points to define the rectangle (NOTE: HAS TO BE CHANGED IF WE WANT TO DRAW THE RECTANGLE)
        elif self.current_tool == "rectangle_selection":
            if self.rectangle_corners is None:
                self.rectangle_corners = (x, y)
                self.window.display_status("Rectangle selection: click the second corner.")
                return 
            #clicked second corner
            x1, y1 = self.rectangle_corners
            self.rectangle_corners = None  # Reset for next selection
            top_left_x = min(x1, x), min(y1, y)
            bottom_right_x = max(x1, x), max(y1, y)
            self.rectangle = (top_left_x, bottom_right_x)

            #display the rectangle on the image
            rectangle_displayed = copy_image(self.current_img)
            rect_color = (0, 255, 255)  # Yellow color for the rectangle
            rect_thickness = 2
            rectangle_displayed = rectangle_selection(rectangle_displayed, top_left_x, bottom_right_x, rect_color, rect_thickness)
            gui_image = convert_opencv_to_gui_image(rectangle_displayed)
            self.window.display_image(gui_image)
            
        elif self.current_tool == "text_tool":
            text = popup_get_text("Enter text to add:", self.window)
            if text is None:
                return
            size = popup_get_integer(3, 1, 100, "Enter text size between 1 and 100", self.window)
            if size is None:
                size = 3
            color = (self.tool_color.blue(), self.tool_color.green(), self.tool_color.red())
            self.history.save(self.current_img)
            # needed for the undo. creates a new image with the text added, so that the undo can revert
            new_image = copy_image(self.current_img)
            # writes the text on the copy
            self.current_img = add_text(new_image, text, (x, y), color, size) 
            self.window.display_image(convert_opencv_to_gui_image(self.current_img))
            
    # selects the shape tool, the shape is drawn by dragging on the image
    def select_shape_tool(self, shape):
        self.current_tool = "draw_shape"
        self.selected_shape = shape
        self.shape_start = None
        self.window.set_draw_mode(True)
        self.window.display_status(
            f"{shape}: drag on the image to draw. Hold Shift for equal sides, Esc to cancel."
        )

    def start_shape(self, x, y):
        if self.current_tool != "draw_shape" or self.current_img is None:
            return
        self.shape_start = (x, y)

    # shows the shape on a copy of the image while the mouse is moving, nothing is saved yet
    def preview_shape(self, x, y, keep_proportions):
        if self.shape_start is None:
            return

        preview = draw_shape(self.current_img, **self._current_shape_info(x, y, keep_proportions))
        self.window.display_image(convert_opencv_to_gui_image(preview))
        end = constrain_end(self.selected_shape, self.shape_start, (x, y), keep_proportions)
        width = abs(end[0] - self.shape_start[0])
        height = abs(end[1] - self.shape_start[1])
        self.window.display_status(f"{self.selected_shape}: {width} x {height} px")

    def finish_shape(self, x, y, keep_proportions):
        if self.shape_start is None:
            return

        end = constrain_end(self.selected_shape, self.shape_start, (x, y), keep_proportions)
        if is_too_small(self.selected_shape, self.shape_start, end):
            self.cancel_shape()
            return

        processed_image = draw_shape(self.current_img, **self._current_shape_info(x, y, keep_proportions))
        self.shape_start = None
        self.history.save(self.current_img)
        self.current_img = processed_image

        gui_image = convert_opencv_to_gui_image(processed_image)
        self.window.display_image(gui_image)
        self.window.display_status(f"{self.selected_shape} drawn. Drag again to draw another one.")

    # stops the shape that is being drawn and shows the image without it
    def cancel_shape(self):
        if self.shape_start is None:
            return

        self.shape_start = None
        self.window.display_image(convert_opencv_to_gui_image(self.current_img))
        self.window.display_status(f"{self.selected_shape}: drag on the image to draw.")

    # everything draw_shape needs for the shape that is being drawn
    def _current_shape_info(self, x, y, keep_proportions):
        fill = self.shape_fill_color
        outline = self.shape_outline_color
        return {
            "shape": self.selected_shape,
            "start": self.shape_start,
            "end": (x, y),
            "fill_color": (fill.blue(), fill.green(), fill.red()),
            "outline_color": (outline.blue(), outline.green(), outline.red()),
            "keep_proportions": keep_proportions,
        }

    # selects the paint brush, painting is done by dragging on the image
    def select_brush_tool(self):
        self.current_tool = "paint_brush"
        self.window.set_draw_mode(True)
        self.window.display_status("Paint brush: drag on the image to paint.")

    def start_brush(self, x, y):
        if self.current_tool != "paint_brush" or self.current_img is None:
            return
        # the whole stroke is one undo step. we paint on a copy because the history keeps the old image
        self.history.save(self.current_img)
        self.current_img = self.current_img.copy()
        self.brush_last = (x, y)
        self._paint_to(x, y)

    def move_brush(self, x, y, keep_proportions):
        if self.brush_last is None:
            return
        self._paint_to(x, y)

    def finish_brush(self, x, y, keep_proportions):
        if self.brush_last is None:
            return
        self._paint_to(x, y)
        self.brush_last = None

    # paints a line from the last point to (x, y), so fast mouse movements do not leave gaps
    def _paint_to(self, x, y):
        color = (self.tool_color.blue(), self.tool_color.green(), self.tool_color.red())
        paint_line(self.current_img, self.brush_last, (x, y), color, self.brush_size)
        self.brush_last = (x, y)
        self.window.display_image(convert_opencv_to_gui_image(self.current_img))

    # selects the object selection tool
    def select_object_tool(self):
        self.current_tool = "select_object"
        self.window.set_draw_mode(False)
        self.window.display_status("Select object: click on an object in the image.")

    def select_rectangle_tool(self):
        self.current_tool = "rectangle_selection"
        self.window.set_draw_mode(False)
        self.rectangle_corners = None  # Reset rectangle corners when selecting the tool
        self.window.display_status("Rectangle selection tool selected. Click at two points to create the rectangle.")

    # crops the image. uses the rectangle defined by the rectangle selection tool
    def crop_image(self):
        if self.current_img is None or self.rectangle is None:
            return

        # corners from the rectangle selection tool
        top_left, bottom_right = self.rectangle
        x0, y0 = top_left
        x1, y1 = bottom_right

        self.history.save(self.current_img)
        self.current_img = crop(self.current_img, x0, x1, y0, y1)
        self.rectangle = None  # Reset the rectangle after cropping
        gui_image = convert_opencv_to_gui_image(self.current_img)
        self.window.display_image(gui_image)

    # selects the text tool
    def select_text_tool(self):
        self.current_tool = "text_tool"
        self.window.set_draw_mode(False)
        self.window.display_status("Text tool selected. Click on the image to add text.")

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

    def select_tool_color(self):
        color = popup_get_color(self.tool_color, "Select tool color", self.window)

        if color is not None:
            self.tool_color = color

    def select_shape_fill_color(self):
        color = popup_get_color(self.shape_fill_color, "Select shape fill color", self.window)

        if color is not None:
            self.shape_fill_color = color

    def select_shape_outline_color(self):
        color = popup_get_color(self.shape_outline_color, "Select shape outline color", self.window)

        if color is not None:
            self.shape_outline_color = color

    def set_brush_size(self):
        size = popup_get_integer(self.brush_size, 1, 1000, "Enter brush size between 1 and 1000", self.window)
                        
        if size is not None:
            self.brush_size = size
