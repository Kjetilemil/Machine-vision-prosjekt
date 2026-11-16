import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QInputDialog,
    QLabel,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence

from controller.controller import Controller
from gui.menubar import create_menubar
from gui.zoomable_label import ZoomableLabel
from gui.style import apply_theme
from gui.menu_icons import add_menu_icons
from gui.tool_panel import ToolPanel, CategoryBar

TOOL_NAMES = {
    "color_picker": "Color picker",
    "select_object": "Select object",
    "rectangle_selection": "Rectangle",
    "freeform_selection": "Free-form",
    "polygon_selection": "Polygon",
    "text_tool": "Text",
    "draw_shape": "Shape",
    "paint_brush": "Paint brush",
    "erase": "Erase",
    "move_object": "Move object",
    "duplicate_object": "Duplicate object",
    "move_paste": "Place pasted image",
}

# initializes the gui
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Item Manipulation")
        self.resize(900, 700)

        self.open_button = QPushButton("Open image")
        title = QLabel("Item Manipulation")
        title.setObjectName("title")
        self.open_button = QPushButton("Open image")
        self.open_button.setObjectName("openButton")
        self.open_button.setCursor(Qt.CursorShape.PointingHandCursor)

        start_screen = QWidget()
        start_layout = QVBoxLayout(start_screen)
        start_layout.addStretch()
        start_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        start_layout.addSpacing(24)
        start_layout.addWidget(self.open_button, alignment=Qt.AlignmentFlag.AlignCenter)
        start_layout.addStretch()

        # creates space in the gui for the imaage
        self.image_label = ZoomableLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # the stack shows one of them at a time: start screen first, then the image
        self.pages = QStackedWidget()
        self.pages.addWidget(start_screen)
        self.pages.addWidget(self.image_label)

        # the tool panel on the left and the image on the right
        self.tool_panel = ToolPanel()
        body = QWidget()
        body_layout = QHBoxLayout(body)
        body_layout.setContentsMargins(0, 0, 0, 0)
        body_layout.setSpacing(0)
        body_layout.addWidget(self.tool_panel)
        body_layout.addWidget(self.pages, 1)

        central = QWidget()
        self.central_layout = QVBoxLayout(central)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(0)
        self.central_layout.addWidget(body, 1)
        self.setCentralWidget(central)
        # the status bar is made right away, otherwise it shows up with the first message
        # and makes the image area smaller, so the image jumps
        self.statusBar()

        # shows which tool is chosen, in the right corner of the status bar
        self.tool_label = QLabel()
        self.tool_label.setObjectName("toolChip")
        self.tool_label.hide()
        self.statusBar().addPermanentWidget(self.tool_label)

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

    # in draw mode dragging on the image draws instead of moving the image
    def set_draw_mode(self, enabled):
        self.image_label.set_draw_mode(enabled)

    def start_zoom_preview(self, zoom_factor, callback):
        self.image_label.start_zoom_preview(zoom_factor, callback)

    def cancel_zoom_preview(self):
        self.image_label.cancel_zoom_preview()

    def set_zoom_factor(self, zoom_factor, image_x=None, image_y=None, view_x=None, view_y=None):
        self.image_label.set_zoom(zoom_factor, image_x, image_y, view_x, view_y)

    # displays a dialog box with the properties of the image
    def display_text(self, text): 
        QMessageBox.information(self, "Properties", text)

    # shows a window with all keyboard shortcuts, read from the menus so the list is always up to date
    def show_keyboard_shortcuts(self):
        actions = []
        for menu_action in self.menuBar().actions():
            actions += menu_action.menu().actions()
        actions += self.actions()  # shortcuts that are not in a menu, like zoom in
        actions = list(dict.fromkeys(actions))  # the menu items are also on the window, so they are removed twice

        rows = []
        for action in actions:
            if action.shortcut().isEmpty():
                continue
            keys = ", ".join(
                key.toString(QKeySequence.SequenceFormat.NativeText) for key in action.shortcuts()
            )
            rows.append((keys, action.statusTip() or action.text()))

        # mouse and trackpad controls are not menu actions, so they are added by hand
        zoom_scroll = "⌘ + scroll" if sys.platform == "darwin" else "Ctrl + scroll"
        rows += [
            ("Arrow keys", "Move the zoomed image"),
            ("Drag / two fingers", "Move the zoomed image"),
            ("Pinch / " + zoom_scroll, "Zoom in and out"),
            ("Drag (shape tool)", "Draw the shape"),
            ("Shift + drag", "Draw with equal sides / straight line"),
            ("Drag (paint brush)", "Paint with the brush color and size"),
            ("Drag (after paste)", "Move the pasted image"),
        ]

        table = "".join(
            f"<tr><td nowrap><b>{keys}</b></td><td nowrap>&nbsp;&nbsp;{text}</td></tr>" for keys, text in rows
        )
        box = QMessageBox(self)
        box.setWindowTitle("Keyboard shortcuts")
        box.setText(f"<table>{table}</table>")
        box.exec()

        # replaces the dropdown menus with a row of menus on top and the tool panel on the left
    def connect_tool_panel(self):
        menu_bar = self.menuBar()
        menus = [action.menu() for action in menu_bar.actions() if action.menu() is not None]

        # the shortcuts stop working when the menu bar is hidden, so the menu items are added to the window too
        for menu in menus:
            for action in menu.actions():
                if action.menu() is not None:
                    self.addActions(action.menu().actions())
                elif not action.isSeparator():
                    self.addAction(action)

        menu_bar.setNativeMenuBar(False)  # on Mac the menu bar would otherwise still be at the top of the screen
        menu_bar.hide()
        self.central_layout.insertWidget(0, CategoryBar(menus, self.tool_panel))

    # shows the name of the chosen tool in the status bar, None hides it
    def show_tool(self, tool):
        self.tool_panel.set_active(tool)
        if tool is None:
            self.tool_label.hide()
            return
        self.tool_label.setText("●  " + TOOL_NAMES.get(tool, tool))
        self.tool_label.show()

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
    apply_theme(app, "dark")

    window = MainWindow()
    controller = Controller(window)
    create_menubar(window, controller)
    add_menu_icons(window.menuBar())
    window.connect_tool_panel()
    window.open_button.clicked.connect(controller.open_image)
    window.image_label.image_clicked.connect(controller.handle_image_click)
    window.image_label.pinch_zoomed.connect(controller.zoom_by)
    window.image_label.drag_started.connect(controller.start_shape)
    window.image_label.drag_moved.connect(controller.preview_shape)
    window.image_label.drag_finished.connect(controller.finish_shape)
    window.image_label.drag_started.connect(controller.start_brush)
    window.image_label.drag_moved.connect(controller.move_brush)
    window.image_label.drag_finished.connect(controller.finish_brush)
    window.image_label.drag_started.connect(controller.start_freeform)
    window.image_label.drag_moved.connect(controller.move_freeform)
    window.image_label.drag_finished.connect(controller.finish_freeform)
    window.image_label.drag_started.connect(controller.start_move)
    window.image_label.drag_moved.connect(controller.preview_move)
    window.image_label.drag_finished.connect(controller.finish_move)
    window.image_label.image_clicked.connect(controller.polygon_click)
    window.image_label.drag_started.connect(controller.start_paste_drag)
    window.image_label.drag_moved.connect(controller.move_paste_drag)
    window.image_label.drag_finished.connect(controller.finish_paste_drag)

    window.show()
    sys.exit(app.exec())
