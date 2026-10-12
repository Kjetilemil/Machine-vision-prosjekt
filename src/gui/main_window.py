import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QInputDialog,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
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

        # start screen with a big button, shown until an image is opened
        self.open_button = QPushButton("Open image")
        self.open_button.setStyleSheet("""
            QPushButton {
                font-size: 18px; padding: 12px 32px; border-radius: 6px;
                background-color: #666666; color: white;
            }
            QPushButton:hover { background-color: #555555; }
        """)
        start_screen = QWidget()
        start_layout = QVBoxLayout(start_screen)
        start_layout.addWidget(self.open_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # creates space in the gui for the imaage
        self.image_label = ZoomableLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # the stack shows one of them at a time: start screen first, then the image
        self.pages = QStackedWidget()
        self.pages.addWidget(start_screen)
        self.pages.addWidget(self.image_label)
        self.setCentralWidget(self.pages)

    def display_image(self, gui_ready_image):
        self.image_label.set_image(gui_ready_image)
        self.pages.setCurrentWidget(self.image_label)

    # arrow keys move the zoomed image
    def keyPressEvent(self, event):
        step = 50
        if event.key() == Qt.Key.Key_Left:
            self.image_label.pan(step, 0)
        elif event.key() == Qt.Key.Key_Right:
            self.image_label.pan(-step, 0)
        elif event.key() == Qt.Key.Key_Up:
            self.image_label.pan(0, step)
        elif event.key() == Qt.Key.Key_Down:
            self.image_label.pan(0, -step)
        else:
            super().keyPressEvent(event)

    def start_zoom_preview(self, zoom_factor, callback):
        self.image_label.start_zoom_preview(zoom_factor, callback)

    def set_zoom_factor(self, zoom_factor, image_x=None, image_y=None, view_x=None, view_y=None):
        self.image_label.set_zoom(zoom_factor, image_x, image_y, view_x, view_y)

    # displays a dialog box with the properties of the image
    def display_text(self, text): 
        QMessageBox.information(self, "Properties", text)

    # displays message in the status bar of the gui
    def display_status(self, text):
        self.statusBar().showMessage(text)

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
    window.open_button.clicked.connect(controller.open_image)
    window.image_label.image_clicked.connect(controller.handle_image_click)
    window.image_label.pinch_zoomed.connect(controller.zoom_by)

    window.show()
    sys.exit(app.exec())
