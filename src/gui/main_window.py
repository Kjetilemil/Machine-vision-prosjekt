import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt6.QtCore import Qt

from controllers import open_image_controller
from gui.menu_options import create_menus


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

        create_menus(self)

    def open_file_system(self):
        open_image_controller.open_file_system(self)

    def display_image(self, gui_ready_image):
        resized_image = gui_ready_image.scaled(
            self.image_label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image_label.setPixmap(resized_image)




def run_main_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
