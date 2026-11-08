
from PyQt6.QtGui import QColor
from image.history import History
from controller.file_controller import open_image, save_image, save_image_as, new_image, run_show_image_properties
from controller.filter_controller import run_apply_gaussian_filter, run_apply_sobel_filter, run_apply_binary_filter, run_apply_histogram_thresholding
from controller.transform_controller import run_rotate_right, run_rotate_left, run_flip_horizontal, run_flip_vertical, run_resize_image, run_crop_image
from controller.object_controller import run_remove_selected_object, run_blur_selected_object, run_recolor_selected_object, run_select_move_tool, run_start_move, run_preview_move, run_finish_move
from controller.clipboard_controller import (
    run_copy_image, run_paste_image, run_cut_image,
    run_start_paste_drag, run_move_paste_drag, run_finish_paste_drag, run_finish_paste, run_cancel_paste,
)
from controller.tool_controller import run_handle_image_click, run_cancel_tool, run_select_color_tool, run_select_object_tool, run_select_rectangle_tool, run_select_text_tool
from controller.shape_controller import run_select_shape_tool, run_start_shape, run_preview_shape, run_finish_shape, run_cancel_shape, run_select_shape_fill_color, run_select_shape_outline_color
from controller.brush_controller import run_select_brush_tool, run_start_brush, run_move_brush, run_finish_brush, run_select_tool_color, run_set_brush_size, run_select_erase_tool
from controller.undo_redo_controller import run_undo, run_redo
from controller.zoom_controller import run_zoom_in, run_zoom_in_directly, run_zoom_by, run_zoom_out
from processing.shapes import SHAPES
from controller.selection_controller import (
    run_select_freeform_tool, run_start_freeform, run_move_freeform, run_finish_freeform,
    run_select_polygon_tool, run_polygon_click,
)

class Controller:
    # current_tool is a property, so the window can show the tool name every time it changes.
    @property
    def current_tool(self):
        return self._current_tool

    @current_tool.setter
    def current_tool(self, tool):
        self._current_tool = tool
        show_tool = getattr(self.window, "show_tool", None)
        if show_tool is not None:
            show_tool(tool)

    def __init__(self, window):
        self.window = window
        self.current_img = None
        self.current_path = None
        self.zoom_factor = 1.0
        self.current_tool = None 
        self.copied_image = None
        self.copied_mask = None  # which pixels of the copied image belong to the selection
        self.floating_paste = None  # the pasted piece while it can still be moved, see clipboard_controller.py
        self.paste_grab = None  # where on the pasted piece the mouse grabbed it
        self.selected_mask = None
        self.move_start = None  # where the drag that moves an object started
        self.move_background = None  # the image the object is placed on while it is moved
        self.history = History()
        self.tool_color = QColor("black")
        self.object_color = QColor("red")
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
        self.selection_points = []  # the points of the free-form or polygon selection being made
        self.selection_type = None  # used for copying and pasting selected objects. rectangle, polygon, or freehand selection



    def open_image(self):
        open_image(self)

    def quit_application(self):
        self.window.close()

    def show_image_properties(self):
        run_show_image_properties(self)

    def undo(self):
        run_undo(self)

    def redo(self):
        run_redo(self)

    def save_image(self):
        save_image(self)

    def save_image_as(self):
        save_image_as(self)

    def apply_gaussian_filter(self):
        run_apply_gaussian_filter(self)

    def apply_sobel_filter(self):
        run_apply_sobel_filter(self)

    def apply_binary_filter(self):
        run_apply_binary_filter(self)

    def apply_histogram_thresholding(self):
        run_apply_histogram_thresholding(self)

    def rotate_right(self):
        run_rotate_right(self)

    def rotate_left(self):
        run_rotate_left(self)

    def flip_horizontal(self):
        run_flip_horizontal(self)

    def flip_vertical(self):
        run_flip_vertical(self)

    def resize_image(self):
        run_resize_image(self)

    def crop_image(self):
        run_crop_image(self)

    def remove_selected_object(self):
        run_remove_selected_object(self)

    def blur_selected_object(self):
        run_blur_selected_object(self)  

    def recolor_selected_object(self):
        run_recolor_selected_object(self)

    # move and duplicate object, the code is in object_controller.py
    def select_move_object_tool(self):
        run_select_move_tool(self, "move_object")

    def select_duplicate_object_tool(self):
        run_select_move_tool(self, "duplicate_object")

    def start_move(self, x, y):
        run_start_move(self, x, y)

    def preview_move(self, x, y, keep_proportions):
        run_preview_move(self, x, y)

    def finish_move(self, x, y, keep_proportions):
        run_finish_move(self, x, y)

    def copy_image(self):
        run_copy_image(self)

    def paste_image(self):
        run_paste_image(self)

    def cut_image(self):
        run_cut_image(self)

    def start_paste_drag(self, x, y):
        run_start_paste_drag(self, x, y)

    def move_paste_drag(self, x, y, keep_proportions):
        run_move_paste_drag(self, x, y)

    def finish_paste_drag(self, x, y, keep_proportions):
        run_finish_paste_drag(self, x, y)

    def finish_paste(self):
        run_finish_paste(self)

    # Esc takes back a paste that is still being moved, otherwise it works like cancel_tool
    def cancel(self):
        if not run_cancel_paste(self):
            run_cancel_tool(self)

    def handle_image_click(self, x, y):
        run_handle_image_click(self, x, y)

    def select_object_tool(self):
        run_select_object_tool(self)

    def select_rectangle_tool(self):
        run_select_rectangle_tool(self)

    def select_text_tool(self):
        run_select_text_tool(self)  

    def select_shape_tool(self, shape):
        run_select_shape_tool(self, shape)

    def start_shape(self, x, y):
        run_start_shape(self, x, y)

    def preview_shape(self, x, y, keep_proportions):
        run_preview_shape(self, x, y, keep_proportions)

    def finish_shape(self, x, y, keep_proportions):
        run_finish_shape(self, x, y, keep_proportions)

    def cancel_shape(self):
        run_cancel_shape(self)

    def cancel_tool(self):
        run_cancel_tool(self)

    def select_shape_fill_color(self):
        run_select_shape_fill_color(self)

    def select_shape_outline_color(self):
        run_select_shape_outline_color(self)

    def select_brush_tool(self):
        run_select_brush_tool(self)

    def start_brush(self, x, y):
        run_start_brush(self, x, y)

    def move_brush(self, x, y, keep_proportions):
        run_move_brush(self, x, y, keep_proportions)

    def finish_brush(self, x, y, keep_proportions):
        run_finish_brush(self, x, y, keep_proportions)

    def select_tool_color(self):
        run_select_tool_color(self) 

    def set_brush_size(self):
        run_set_brush_size(self)

    def new_image(self):
        new_image(self)

    # selects the color picker tool
    def select_color_tool(self):
        run_select_color_tool(self)


    def zoom_in(self):
        run_zoom_in(self)

    def zoom_in_directly(self):
        run_zoom_in_directly(self)

    def zoom_by(self, factor):
        run_zoom_by(self, factor)

    def zoom_out(self):
        run_zoom_out(self)

    def select_erase_tool(self):
        run_select_erase_tool(self)
        

    # free-form and polygon selection, the code is in selection_controller.py
    def select_freeform_tool(self):
        run_select_freeform_tool(self)

    def start_freeform(self, x, y):
        run_start_freeform(self, x, y)

    def move_freeform(self, x, y, keep_proportions):
        run_move_freeform(self, x, y)

    def finish_freeform(self, x, y, keep_proportions):
        run_finish_freeform(self, x, y)

    def select_polygon_tool(self):
        run_select_polygon_tool(self)

    def polygon_click(self, x, y):
        run_polygon_click(self, x, y)

    # returns the area of the image defined by the rectangle selection tool - used for copying and pasting selected areas
    def get_selected_area(self):
        top_left, bottom_right = self.rectangle
        x0, y0 = top_left
        x1, y1 = bottom_right
        return self.current_img[y0:y1, x0:x1]
