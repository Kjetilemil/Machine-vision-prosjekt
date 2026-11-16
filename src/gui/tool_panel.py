from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QKeySequence
from PyQt6.QtGui import QIcon, QKeySequence, QPixmap
from PyQt6.QtWidgets import (
    QButtonGroup,
    QHBoxLayout,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from gui.menu_icons import ICONS, _paint_icon
from gui.style import current_colors

# these menus are not tools, so they open as a normal dropdown instead of in the panel
DROPDOWN_MENUS = ("&File", "&Help")

# the menu that is shown in the panel when the app starts
START_MENU = "&Image"

# which menu item belongs to each tool, so the chosen tool can light up
TOOL_ACTIONS = {
    "rectangle_selection": "Select Rectangular",
    "freeform_selection": "Select Free-form",
    "polygon_selection": "Select polygon",
    "select_object": "Select object",
    "move_object": "Move object",
    "duplicate_object": "Duplicate object",
    "erase": "Erase",
    "color_picker": "Color picker",
    "paint_brush": "Paint brush",
    "text_tool": "Text box",
}


def panel_icon(text):
    """Grey icon, lighter when the mouse is over it, and blue when the tool is chosen."""
    icon = QIcon()
    if text not in ICONS:
        empty = QPixmap(48, 48)
        empty.fill(Qt.GlobalColor.transparent)
        icon.addPixmap(empty)
        return icon
    colors = current_colors()
    name = ICONS[text]
    icon.addPixmap(_paint_icon(name, colors["muted"]), QIcon.Mode.Normal, QIcon.State.Off)
    icon.addPixmap(_paint_icon(name, colors["text"]), QIcon.Mode.Active, QIcon.State.Off)
    icon.addPixmap(_paint_icon(name, colors["accent"]), QIcon.Mode.Normal, QIcon.State.On)
    icon.addPixmap(_paint_icon(name, colors["accent"]), QIcon.Mode.Active, QIcon.State.On)
    return icon


class ToolPanel(QWidget):
    """Panel on the left that shows the items of the chosen menu as buttons."""

    def __init__(self):
        super().__init__()
        self.setObjectName("toolPanel")
        self.setFixedWidth(240)
        self.buttons = {}
        self.active_tool = None

        self.list = QWidget()
        self.list_layout = QVBoxLayout(self.list)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(2)

        scroll = QScrollArea()  # in case a menu has more items than there is room for
        scroll.setWidget(self.list)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.addWidget(scroll)

    # shows the items of a menu, clicking a button does the same as clicking the item in the menu
    def show_menu(self, menu):
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)  # takes it off the panel right away
                widget.deleteLater()
        self.buttons = {}

        for action in menu.actions():
            if action.isSeparator():
                continue
            # a menu inside the menu (like the list of shapes) gets a small heading and its own buttons
            if action.menu() is not None:
                heading = QLabel(action.text())
                heading.setObjectName("panelHeading")
                self.list_layout.addWidget(heading)
                for sub_action in action.menu().actions():
                    self._add_button(sub_action)
                continue
            self._add_button(action)

        self.list_layout.addStretch()
        self.set_active(self.active_tool)

    def _add_button(self, action):
        button = QToolButton()
        button.setText(action.text())
        button.setToolTip(action.statusTip())
        button.setIcon(panel_icon(action.text()))
        button.setIconSize(QSize(18, 18))
        button.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button.setCursor(Qt.CursorShape.PointingHandCursor)
        # only tools stay lit up, actions like Rotate just happen once
        button.setCheckable(action.text() in TOOL_ACTIONS.values())
        button.clicked.connect(action.trigger)

        # the shortcut is shown on the right side of the button, like in a menu
        shortcut = action.shortcut().toString(QKeySequence.SequenceFormat.NativeText)
        if shortcut:
            label = QLabel(shortcut)
            label.setObjectName("panelShortcut")
            label.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)  # clicks go to the button
            row = QHBoxLayout(button)
            row.setContentsMargins(0, 0, 10, 0)
            row.addStretch()
            row.addWidget(label)

        self.list_layout.addWidget(button)
        self.buttons[action.text()] = button

    # lights up the button of the chosen tool
    def set_active(self, tool):
        self.active_tool = tool
        active_text = TOOL_ACTIONS.get(tool)
        for text, button in self.buttons.items():
            if button.isCheckable():
                button.setChecked(text == active_text)


class CategoryBar(QWidget):
    """The row at the top. File and Help open a dropdown, the other menus are shown in the panel."""

    def __init__(self, menus, panel):
        super().__init__()
        self.setObjectName("categoryBar")
        self.tabs = QButtonGroup(self)  # only one tab can be chosen at a time
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        layout.setSpacing(2)

        for menu in menus:
            button = QToolButton()
            button.setText(menu.title().replace("&", ""))
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            if menu.title() in DROPDOWN_MENUS:
                button.setMenu(menu)
                button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
            else:
                button.setCheckable(True)
                self.tabs.addButton(button)
                button.clicked.connect(lambda checked=False, menu=menu: panel.show_menu(menu))
                if menu.title() == START_MENU:
                    button.setChecked(True)
                    panel.show_menu(menu)
            if menu.title() == "&Help":
                layout.addStretch()  # Help is placed on the right side
            layout.addWidget(button)