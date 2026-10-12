from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import QMenu, QMainWindow
from controller.controller import Controller

def add_menu_action(menu: QMenu, action_name: str, func: callable = None, shortcut=None, description=None):
    action = QAction(action_name, menu)
    
    if func is not None:
        action.triggered.connect(func)

    # a list gives the action more than one shortcut, e.g. both Delete and Backspace
    if isinstance(shortcut, list):
        action.setShortcuts(shortcut)
    elif shortcut is not None:
        action.setShortcut(shortcut)

    # the description is shown in the status bar and in the keyboard shortcuts window
    if description is not None:
        action.setStatusTip(description)
    
    menu.addAction(action)

def create_menubar(window: QMainWindow, controller: Controller):
    menu_bar = window.menuBar()

    file_menu = menu_bar.addMenu("&File")
    add_menu_action(file_menu, "New", controller.new_image, QKeySequence("Ctrl+N"), "Create a blank image")
    add_menu_action(file_menu, "Open", controller.open_image, QKeySequence("Ctrl+O"), "Open an image")
    add_menu_action(file_menu, "Save", controller.save_image, QKeySequence("Ctrl+S"), "Save the image")
    add_menu_action(file_menu, "Save as", controller.save_image_as, QKeySequence("Ctrl+Shift+S"), "Save the image as a new file")
    add_menu_action(file_menu, "Properties", controller.show_image_properties)
    add_menu_action(file_menu, "Quit", controller.quit_application, QKeySequence("Ctrl+Q"), "Quit the program")

    # Qt turns "Ctrl" into Cmd on Mac, so this is Cmd+Z / Cmd+Y on Mac and Ctrl+Z / Ctrl+Y on Windows
    edit_menu = menu_bar.addMenu("&Edit")
    add_menu_action(edit_menu, "Undo", controller.undo, QKeySequence.StandardKey.Undo, "Undo the last change")
    add_menu_action(edit_menu, "Redo", controller.redo, QKeySequence("Ctrl+Y"), "Redo the change that was undone")

    clipboard_menu = menu_bar.addMenu("&Clipboard")
    add_menu_action(clipboard_menu, "Copy", controller.copy_image, QKeySequence("Ctrl+C"), "Copy the image")
    add_menu_action(clipboard_menu, "Paste", controller.paste_image, QKeySequence("Ctrl+V"), "Paste the copied image")
    add_menu_action(clipboard_menu, "Cut", controller.cut_image, QKeySequence("Ctrl+X"), "Cut the image")

    image_menu = menu_bar.addMenu("&Image")
    add_menu_action(image_menu, "Select Rectangular")
    add_menu_action(image_menu, "Select Free-form")
    add_menu_action(image_menu, "Select polygon")
    add_menu_action(image_menu, "Crop")
    add_menu_action(image_menu, "Resize", controller.resize_image)
    add_menu_action(image_menu, "Rotate right 90", controller.rotate_right, QKeySequence("Ctrl+R"), "Rotate the image right")
    add_menu_action(image_menu, "Rotate left 90", controller.rotate_left, QKeySequence("Ctrl+L"), "Rotate the image left")
    add_menu_action(image_menu, "Flip vertical", controller.flip_vertical)
    add_menu_action(image_menu, "Flip Horizontal", controller.flip_horizontal)
    # single keys, like the tool keys in other image editors
    add_menu_action(image_menu, "Select object", controller.select_object_tool, QKeySequence("S"), "Click on an object to select it")
    add_menu_action(
        image_menu,
        "Remove object",
        controller.remove_selected_object,
        [QKeySequence("Backspace"), QKeySequence("Delete")],
        "Remove the selected object",
    )
    add_menu_action(image_menu, "Blur object", controller.blur_selected_object, QKeySequence("B"), "Blur the selected object")
    add_menu_action(image_menu, "Change object color", controller.shift_selected_object_color, QKeySequence("C"), "Change color of selected object")

    tools_menu = menu_bar.addMenu("&Tools")
    add_menu_action(tools_menu, "Zoom in", controller.zoom_in)
    add_menu_action(tools_menu, "Zoom out", controller.zoom_out, QKeySequence("Ctrl+-"), "Zoom out")
    add_menu_action(tools_menu, "Erase")
    add_menu_action(tools_menu, "Color picker", controller.select_color_tool, QKeySequence("I"), "Click on the image to see the color")
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

    # Cmd/Ctrl + zooms in right away, so it is not in a menu ("Zoom in" in Tools asks for a point)
    add_menu_action(window, "Zoom in", controller.zoom_in_directly, QKeySequence("Ctrl++"), "Zoom in")

    color_menu = menu_bar.addMenu("&Colors")
    add_menu_action(color_menu, "Color palette")
    add_menu_action(color_menu, "Brush size")

    # Cmd+? on Mac and F1 on Windows
    help_menu = menu_bar.addMenu("&Help")
    add_menu_action(
        help_menu,
        "Keyboard shortcuts",
        window.show_keyboard_shortcuts,
        QKeySequence.StandardKey.HelpContents,
        "Show all keyboard shortcuts",
    )
