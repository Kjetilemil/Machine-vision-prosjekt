from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu, QMainWindow
from controller.controller import Controller

def add_menu_action(menu: QMenu, action_name: str, func: callable = None):
    action = QAction(action_name, menu)
    
    if func is not None:
        action.triggered.connect(func)
    
    menu.addAction(action)

def create_menubar(window: QMainWindow, controller: Controller):
    menu_bar = window.menuBar()

    file_menu = menu_bar.addMenu("&File")
    add_menu_action(file_menu, "New")
    add_menu_action(file_menu, "Open", controller.open_image)
    add_menu_action(file_menu, "Save", controller.save_image)
    add_menu_action(file_menu, "Save as", controller.save_image_as)
    add_menu_action(file_menu, "Properties")
    add_menu_action(file_menu, "Quit")

    clipboard_menu = menu_bar.addMenu("&Clipboard")
    add_menu_action(clipboard_menu, "Copy")
    add_menu_action(clipboard_menu, "Paste")
    add_menu_action(clipboard_menu, "Cut")

    image_menu = menu_bar.addMenu("&Image")
    add_menu_action(image_menu, "Select Rectangular")
    add_menu_action(image_menu, "Select Free-form")
    add_menu_action(image_menu, "Select polygon")
    add_menu_action(image_menu, "Crop")
    add_menu_action(image_menu, "Resize")
    add_menu_action(image_menu, "Rotate right 90", controller.rotate_right)
    add_menu_action(image_menu, "Rotate left 90", controller.rotate_left)
    add_menu_action(image_menu, "Flip vertical", controller.flip_vertical)
    add_menu_action(image_menu, "Flip Horizontal", controller.flip_horizontal)

    tools_menu = menu_bar.addMenu("&Tools")
    add_menu_action(tools_menu, "Zoom in")
    add_menu_action(tools_menu, "Zoom out")
    add_menu_action(tools_menu, "Erase")
    add_menu_action(tools_menu, "Color picker")
    add_menu_action(tools_menu, "Paint brush")
    add_menu_action(tools_menu, "Text box")
    add_menu_action(tools_menu, "Gaussian filter", controller.apply_gaussian_filter)
    add_menu_action(tools_menu, "Sobel filter", controller.apply_sobel_filter)
    add_menu_action(tools_menu, "Binary filter", controller.apply_binary_filter)
    add_menu_action(tools_menu, "Histogram thresholding", controller.apply_histogram_thresholding)

    shapes_menu = menu_bar.addMenu("&Shapes")
    add_menu_action(shapes_menu, "List of shapes")
    add_menu_action(shapes_menu, "Outline color")
    add_menu_action(shapes_menu, "Fill color")

    color_menu = menu_bar.addMenu("&Colors")
    add_menu_action(color_menu, "Color palette")
    add_menu_action(color_menu, "Brush size")
