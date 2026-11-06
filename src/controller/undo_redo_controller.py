from image.convert_image_for_gui import convert_opencv_to_gui_image


# goes back to the image before the last change
def run_undo(controller):
        previous_image = controller.history.undo(controller.current_img)
        if previous_image is None:
            controller.window.display_status("Nothing to undo.")
            return

        controller.current_img = previous_image
        controller.window.display_image(convert_opencv_to_gui_image(controller.current_img))
        controller.window.display_status("Undo.")


# brings back the change that was undone
def run_redo(controller):
        next_image = controller.history.redo(controller.current_img)
        if next_image is None:
            controller.window.display_status("Nothing to redo.")
            return

        controller.current_img = next_image
        controller.window.display_image(convert_opencv_to_gui_image(controller.current_img))
        controller.window.display_status("Redo.")