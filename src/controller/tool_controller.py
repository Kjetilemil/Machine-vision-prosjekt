from image.convert_image_for_gui import convert_opencv_to_gui_image
from image.properties import get_image_properties, get_pixel_color
from image.copy import copy_image
from processing.object_selection import select_object, draw_selection
from processing.rectangle_selection import rectangle_selection
from processing.clipboard import rectangle_mask
from processing.text import add_text
from gui.popup import popup_get_integer, popup_get_color, popup_get_text




def run_handle_image_click(controller, x, y):
        if controller.current_tool == "color_picker":
            if controller.current_img is None:
                return

            blue, green, red = get_pixel_color(controller.current_img, x, y)
            color_info = f"Color at ({x}, {y}): R={red}, G={green}, B={blue}"
            controller.window.display_status(color_info)

        elif controller.current_tool == "select_object":
            if controller.current_img is None:
                return
            mask = select_object(controller.current_img, x, y)
            if not mask.any():
                controller.window.display_status("Could not find an object there.")
                return
            controller.selected_mask = mask
            controller.selection_type = "object"
            controller.rectangle = None  # the new selection replaces an old rectangle
            pixels = int((mask > 0).sum())
            controller.window.display_status(f"Object selected ({pixels} pixels)")
            preview = draw_selection(controller.current_img, mask)
            controller.window.display_image(convert_opencv_to_gui_image(preview))

        # rectangle selection tool. User clicks two points to define the rectangle (NOTE: HAS TO BE CHANGED IF WE WANT TO DRAW THE RECTANGLE)
        elif controller.current_tool == "rectangle_selection":
            if controller.rectangle_corners is None:
                controller.rectangle_corners = (x, y)
                controller.window.display_status("Rectangle selection: click the second corner.")
                return 
            #clicked second corner
            x1, y1 = controller.rectangle_corners
            controller.rectangle_corners = None  # Reset for next selection
            top_left_x = min(x1, x), min(y1, y)
            bottom_right_x = max(x1, x), max(y1, y)
            controller.rectangle = (top_left_x, bottom_right_x)
            controller.selection_type = "rectangle"
            # every selection is also a mask, so remove, blur, move, copy and crop work the same for all of them
            mask = rectangle_mask(controller.current_img, top_left_x, bottom_right_x)
            # an empty rectangle (both clicks on the same line) is no selection
            controller.selected_mask = mask if mask.any() else None

            #display the rectangle on the image
            rectangle_displayed = copy_image(controller.current_img)
            rect_color = (0, 255, 255)  # Yellow color for the rectangle
            rect_thickness = 2
            rectangle_displayed = rectangle_selection(rectangle_displayed, top_left_x, bottom_right_x, rect_color, rect_thickness)
            gui_image = convert_opencv_to_gui_image(rectangle_displayed)
            controller.window.display_image(gui_image)
            
        elif controller.current_tool == "text_tool":
            text = popup_get_text("Enter text to add:", controller.window)
            if text is None:
                return
            size = popup_get_integer(3, 1, 100, "Enter text size between 1 and 100", controller.window)
            if size is None:
                size = 3
            color = (controller.tool_color.blue(), controller.tool_color.green(), controller.tool_color.red())
            controller.history.save(controller.current_img)
            # needed for the undo. creates a new image with the text added, so that the undo can revert
            new_image = copy_image(controller.current_img)
            # writes the text on the copy
            controller.current_img = add_text(new_image, text, (x, y), color, size) 
            controller.window.display_image(convert_opencv_to_gui_image(controller.current_img))


def run_select_color_tool(controller):
        controller.current_tool = "color_picker"
        controller.window.set_draw_mode(False)
        controller.window.display_status("Color picker tool selected. Click on the image to pick a color.")

# selects the object selection tool
def run_select_object_tool(controller):
        controller.current_tool = "select_object"
        controller.window.set_draw_mode(False)
        controller.window.display_status("Select object: click on an object in the image.")


def run_select_rectangle_tool(controller):
        controller.current_tool = "rectangle_selection"
        controller.window.set_draw_mode(False)
        controller.rectangle_corners = None  # Reset rectangle corners when selecting the tool
        controller.window.display_status("Rectangle selection tool selected. Click at two points to create the rectangle.")


# selects the text tool
def run_select_text_tool(controller):
        controller.current_tool = "text_tool"
        controller.window.set_draw_mode(False)
        controller.window.display_status("Text tool selected. Click on the image to add text.")


# Esc stops a shape or move that is being dragged.
# if nothing is being dragged it leaves the tool and the selection, like when the app has just started
def run_cancel_tool(controller):
        if controller.shape_start is not None:
            controller.cancel_shape()
            return

        if controller.move_start is not None:
            controller.move_start = None
            controller.move_background = None
            controller.window.display_image(convert_opencv_to_gui_image(controller.current_img))
            controller.window.display_status("Move cancelled.")
            return

        controller.current_tool = None
        controller.selected_mask = None
        controller.selection_type = None
        controller.selection_points = []
        controller.rectangle = None
        controller.rectangle_corners = None
        controller.brush_last = None
        controller.window.set_draw_mode(False)
        controller.window.cancel_zoom_preview()
        if controller.current_img is not None:
            controller.window.display_image(convert_opencv_to_gui_image(controller.current_img))
        controller.window.display_status("No tool selected.")
