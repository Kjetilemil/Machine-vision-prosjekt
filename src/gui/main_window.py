import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox, QInputDialog
from PyQt6.QtCore import Qt

from controller.controller import Controller
from gui.menubar import create_menubar


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
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.image_label)

    def display_image(self, gui_ready_image):
        resized_image = gui_ready_image.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(resized_image)

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
