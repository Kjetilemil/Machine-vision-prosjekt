import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
from PyQt6.QtCore import Qt

from controller.controller import Controller
from gui.menubar import create_menubar
from gui.zoomable_label import ZoomableLabel


# initializes the gui
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image editor")
        self.resize(900, 700)
        self.setStyleSheet("""
            QMainWindow { background-color: #d3d3d3; }
            QMenuBar { background-color: #666666; }
        """)

        # creates space in the gui for the imaage
        self.image_label = ZoomableLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.image_label)

    def display_image(self, gui_ready_image):
        self.image_label.set_image(gui_ready_image)

    def start_zoom_preview(self, zoom_factor, callback):
        self.image_label.start_zoom_preview(zoom_factor, callback)

    def set_zoom_factor(self, zoom_factor, image_x=None, image_y=None, view_x=None, view_y=None):
        self.image_label.set_zoom(zoom_factor, image_x, image_y, view_x, view_y)

    # displays a dialog box with the properties of the image
    def display_text(self, text):
        QMessageBox.information(self, "Properties", text)

    # dialog box for asking the user for new dimensions when resizing an image
    def ask_for_resize_dimensions(self):
        width, ok_width = QInputDialog.getInt(self, "Resize Image", "Enter new width:")
        if not ok_width:
            return None, None

        height, ok_height = QInputDialog.getInt(self, "Resize Image", "Enter new height:")
        if not ok_height:
            return None, None

        return width, height

def run_main_window():
    app = QApplication(sys.argv)

    window = MainWindow()
    controller = Controller(window)
    create_menubar(window, controller)

    window.show()
    sys.exit(app.exec())
