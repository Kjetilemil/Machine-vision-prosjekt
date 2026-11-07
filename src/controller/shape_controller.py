from image.convert_image_for_gui import convert_opencv_to_gui_image
from gui.popup import popup_get_color
from processing.shapes import draw_shape, constrain_end, is_too_small


# selects the shape tool, the shape is drawn by dragging on the image
def run_select_shape_tool(controller, shape):
        controller.current_tool = "draw_shape"
        controller.selected_shape = shape
        controller.shape_start = None
        controller.window.set_draw_mode(True)
        controller.window.display_status(
            f"{shape}: drag on the image to draw. Hold Shift for equal sides, Esc to cancel."
        )

def run_start_shape(controller, x, y):
        if controller.current_tool != "draw_shape" or controller.current_img is None:
            return
        controller.shape_start = (x, y)

# shows the shape on a copy of the image while the mouse is moving, nothing is saved yet
def run_preview_shape(controller, x, y, keep_proportions):
        if controller.shape_start is None:
            return

        preview = draw_shape(controller.current_img, **run__current_shape_info(controller, x, y, keep_proportions))
        controller.window.display_image(convert_opencv_to_gui_image(preview))
        end = constrain_end(controller.selected_shape, controller.shape_start, (x, y), keep_proportions)
        width = abs(end[0] - controller.shape_start[0])
        height = abs(end[1] - controller.shape_start[1])
        controller.window.display_status(f"{controller.selected_shape}: {width} x {height} px")


def run_finish_shape(controller, x, y, keep_proportions):
        if controller.shape_start is None:
            return

        end = constrain_end(controller.selected_shape, controller.shape_start, (x, y), keep_proportions)
        if is_too_small(controller.selected_shape, controller.shape_start, end):
            controller.cancel_shape()
            return

        processed_image = draw_shape(controller.current_img, **run__current_shape_info(controller, x, y, keep_proportions))
        controller.shape_start = None
        controller.history.save(controller.current_img)
        controller.current_img = processed_image

        gui_image = convert_opencv_to_gui_image(processed_image)
        controller.window.display_image(gui_image)
        controller.window.display_status(f"{controller.selected_shape} drawn. Drag again to draw another one.")


# stops the shape that is being drawn and shows the image without it
def run_cancel_shape(controller):
        if controller.shape_start is None:
            return

        controller.shape_start = None
        controller.window.display_image(convert_opencv_to_gui_image(controller.current_img))
        controller.window.display_status(f"{controller.selected_shape}: drag on the image to draw.")

# everything draw_shape needs for the shape that is being drawn
def run__current_shape_info(controller, x, y, keep_proportions):
        fill = controller.shape_fill_color
        outline = controller.shape_outline_color
        return {
            "shape": controller.selected_shape,
            "start": controller.shape_start,
            "end": (x, y),
            "fill_color": (fill.blue(), fill.green(), fill.red()),
            "outline_color": (outline.blue(), outline.green(), outline.red()),
            "keep_proportions": keep_proportions,
        }

def run_select_shape_fill_color(controller):
        color = popup_get_color(controller.shape_fill_color, "Select shape fill color", controller.window)

        if color is not None:
            controller.shape_fill_color = color

def run_select_shape_outline_color(controller):
        color = popup_get_color(controller.shape_outline_color, "Select shape outline color", controller.window)

        if color is not None:
            controller.shape_outline_color = color

