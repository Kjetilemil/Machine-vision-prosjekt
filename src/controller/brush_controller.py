from image.convert_image_for_gui import convert_opencv_to_gui_image
from gui.popup import popup_get_integer, popup_get_color
from processing.brush import paint_line


# selects the paint brush, painting is done by dragging on the image
def run_select_brush_tool(controller):
        controller.current_tool = "paint_brush"
        controller.window.set_draw_mode(True)
        controller.window.display_status("Paint brush: drag on the image to paint.")


def run_start_brush(controller, x, y):
        if controller.current_tool != "paint_brush" or controller.current_img is None:
            return
        # the whole stroke is one undo step. we paint on a copy because the history keeps the old image
        controller.history.save(controller.current_img)
        controller.current_img = controller.current_img.copy()
        controller.brush_last = (x, y)
        run__paint_to(controller, x, y)


def run_move_brush(controller, x, y, keep_proportions):
        if controller.brush_last is None:
            return
        run__paint_to(controller, x, y)


def run_finish_brush(controller, x, y, keep_proportions):
        if controller.brush_last is None:
            return
        run__paint_to(controller, x, y)
        controller.brush_last = None


# paints a line from the last point to (x, y), so fast mouse movements do not leave gaps
def run__paint_to(controller, x, y):
        color = (controller.tool_color.blue(), controller.tool_color.green(), controller.tool_color.red())
        paint_line(controller.current_img, controller.brush_last, (x, y), color, controller.brush_size)
        controller.brush_last = (x, y)
        controller.window.display_image(convert_opencv_to_gui_image(controller.current_img))


def run_select_tool_color(controller):
        color = popup_get_color(controller.tool_color, "Select tool color", controller.window)

        if color is not None:
            controller.tool_color = color


def run_set_brush_size(controller):
        size = popup_get_integer(controller.brush_size, 1, 1000, "Enter brush size between 1 and 1000", controller.window)
                        
        if size is not None:
            controller.brush_size = size





