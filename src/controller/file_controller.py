from pathlib import Path

from PyQt6.QtWidgets import QFileDialog
from image.filesystem import filesystem_open_image, filesystem_save_image
from image.convert_image_for_gui import convert_opencv_to_gui_image
from image.blank_canvas import run_blank_canvas


# function to access files and select image, processes the image and displays it  
def open_image(controller):
    image_file_name, _ = QFileDialog.getOpenFileName(controller.window, 'Open File')

    if image_file_name:
        try:
            cv_image = filesystem_open_image(image_file_name)
            controller.current_img = cv_image
            controller.current_path = image_file_name
            gui_image = convert_opencv_to_gui_image(cv_image)
            controller.window.display_image(gui_image)
        except ValueError as error:
            print(error)


def save_image(controller):
    if controller.current_img is None:
        return

    if controller.current_path is None:
        save_image_as(controller)
        return

    try:
        filesystem_save_image(controller.current_path, controller.current_img)
    except ValueError as error:
        print(error)


def save_image_as(controller):
    if controller.current_img is None:
        return

    image_file_name, selected_filter = QFileDialog.getSaveFileName(
        controller.window,
        'Save File',
        '',
        'PNG image (*.png);;JPEG image (*.jpg *.jpeg);;BMP image (*.bmp);;TIFF image (*.tif *.tiff)',
    )
    if image_file_name:
        if not Path(image_file_name).suffix or image_file_name.endswith('.'):
            extension = next(
                (extension for extension in ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')
                 if f'*{extension}' in selected_filter),
                '.png',
            )
            image_file_name = image_file_name.rstrip('.') + extension
        try:
            filesystem_save_image(image_file_name, controller.current_img)
            controller.current_path = image_file_name
        except ValueError as error:
            print(error)


#creates a blank canvas by pressing new
def new_image(controller):
    
    cv_image = run_blank_canvas()
    controller.current_img = cv_image
    controller.current_path = None
    gui_image = convert_opencv_to_gui_image(cv_image)
    controller.window.display_image(gui_image)
