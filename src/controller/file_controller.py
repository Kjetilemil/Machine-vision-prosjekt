from PyQt6.QtWidgets import QFileDialog
from image.filesystem import filesystem_open_image, filesystem_save_image
from image.convert_image_for_gui import convert_opencv_to_gui_image


# function to access files and select image, processes the image and displays it  
def open_image(controller):
    image_file_name, _ = QFileDialog.getOpenFileName(controller.window, 'Open File')

    if image_file_name:
        try:
            cv_image = filesystem_open_image(image_file_name)
            controller.current_img = cv_image
            gui_image = convert_opencv_to_gui_image(cv_image)
            controller.window.display_image(gui_image)
        except ValueError as error:
            print(error)

def save_image(controller):
    image_file_name, _ = QFileDialog.getSaveFileName(controller.window, 'Save File')

    print(image_file_name)
    
    if image_file_name:
        try:
            filesystem_save_image(image_file_name, controller.current_img)

        except ValueError as error:
            print(error)
