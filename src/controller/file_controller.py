from PyQt6.QtWidgets import QFileDialog
from image.filesystem import open_image
from image.convert_image_for_gui import convert_opencv_to_gui_image


# function to access files and select image, processes the image and displays it  
def handle_open_image(main_window):
    image_file_name, _ = QFileDialog.getOpenFileName(main_window, 'Open File')

    if image_file_name:
        try:
            cv_image = open_image(image_file_name)
            gui_image = convert_opencv_to_gui_image(cv_image)
            main_window.display_image(gui_image)
        except ValueError as error:
            print(error)