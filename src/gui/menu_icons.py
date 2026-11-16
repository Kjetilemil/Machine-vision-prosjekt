from pathlib import Path

from PyQt6.QtCore import QByteArray, Qt
from PyQt6.QtGui import QIcon, QPainter, QPixmap
from PyQt6.QtSvg import QSvgRenderer

from gui.style import current_colors

# the icons are from Lucide (https://lucide.dev), see the LICENSE file in the icons folder
ICON_FOLDER = Path(__file__).parent / "icons"

# icon for each menu item, items that are not here are shown without an icon
ICONS = {
    "Undo": "undo-2",
    "Redo": "redo-2",
    "Copy": "copy",
    "Paste": "clipboard-paste",
    "Cut": "scissors",
    "Select Rectangular": "square-dashed",
    "Select Free-form": "lasso",
    "Select polygon": "pentagon",
    "Select object": "mouse-pointer-click",
    "Crop": "crop",
    "Resize": "scaling",
    "Rotate right 90": "rotate-cw",
    "Rotate left 90": "rotate-ccw",
    "Flip vertical": "flip-vertical-2",
    "Flip Horizontal": "flip-horizontal-2",
    "Remove object": "trash-2",
    "Blur object": "droplet",
    "Change object color": "palette",
    "Move object": "move",
    "Duplicate object": "copy-plus",
    "Zoom in": "zoom-in",
    "Zoom out": "zoom-out",
    "Erase": "eraser",
    "Color picker": "pipette",
    "Paint brush": "brush",
    "Text box": "type",
    "Gaussian filter": "droplets",
    "Sobel filter": "scan-line",
    "Binary filter": "contrast",
    "Histogram thresholding": "chart-column",
    "List of shapes": "shapes",
    "Outline color": "palette",
    "Fill color": "palette",
    "Brush color": "palette",
    "Brush size": "circle-dot",
}


def _paint_icon(name, color):
    """Paints an icon from the icons folder in the given color."""
    svg = (ICON_FOLDER / f"{name}.svg").read_text().replace("currentColor", color)
    pixmap = QPixmap(48, 48)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    QSvgRenderer(QByteArray(svg.encode())).render(painter)
    painter.end()
    return pixmap


def load_icon(name):
    colors = current_colors()
    icon = QIcon()
    icon.addPixmap(_paint_icon(name, colors["muted"]), QIcon.Mode.Normal)
    # the item under the mouse has a blue background, so its icon is painted white
    icon.addPixmap(_paint_icon(name, colors["accent_text"]), QIcon.Mode.Active)
    return icon


def add_menu_icons(menu_bar):
    """Gives every menu item that is in ICONS its icon, also the items in menus inside menus."""
    menus = [action.menu() for action in menu_bar.actions() if action.menu() is not None]
    while menus:
        menu = menus.pop()
        for action in menu.actions():
            if action.text() in ICONS:
                action.setIcon(load_icon(ICONS[action.text()]))
            if action.menu() is not None:
                menus.append(action.menu())