from PyQt6.QtGui import QAction


# menu bar options
def create_menus(window):
        menu_bar = window.menuBar()

        # File menu
        file_menu = menu_bar.addMenu("&file")
        file_menu.addAction("New")

        open_new = QAction("open", window)
        open_new.triggered.connect(window.open_file_system)
        file_menu.addAction(open_new)

        file_menu.addAction("Save")
        file_menu.addAction("Save as")
        file_menu.addAction("Properties")
        file_menu.addAction("Quit")
        
        # Clipboard menu
        clipboard_menu = menu_bar.addMenu("&clipboard")
        clipboard_menu.addAction("Copy")
        clipboard_menu.addAction("Paste")
        clipboard_menu.addAction("Cut")

        # Image Menu
        image_menu = menu_bar.addMenu("&image")
        image_menu.addAction("Select Rectangular")
        image_menu.addAction("Select Free-form")
        image_menu.addAction("Select polygon")
        image_menu.addAction("Crop")
        image_menu.addAction("Resize")
        image_menu.addAction("Rotate right 90")
        image_menu.addAction("Rotate left 90")
        image_menu.addAction("Flip vertical")
        image_menu.addAction("Flip Horizontal")

        # Tools menu
        tools_menu = menu_bar.addMenu("&tools")
        tools_menu.addAction("Zoom in")
        tools_menu.addAction("Zoom out")
        tools_menu.addAction("Erase")
        tools_menu.addAction("Color picker")
        tools_menu.addAction("Paint brush")
        tools_menu.addAction("Text box")
        tools_menu.addAction("Gaussian filter")
        tools_menu.addAction("Soble filter")
        tools_menu.addAction("Binary filter")
        tools_menu.addAction("Histogram thresholding")

        # Shapes menu 
        shapes_menu = menu_bar.addMenu("&shapes")
        shapes_menu.addAction("List of shapes")
        shapes_menu.addAction("Outline color")
        shapes_menu.addAction("Fill color")

        # Color menu
        color_menu = menu_bar.addMenu("&colors")
        color_menu.addAction("Color palette")
        color_menu.addAction("Brush size")