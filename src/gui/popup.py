from PyQt6.QtWidgets import QInputDialog, QColorDialog
from PyQt6.QtGui import QColor

def popup_get_integer(default: int, vmin: int, vmax: int, text: str, window) -> int:
    value, ok = QInputDialog.getInt(window, "Input", text, default, vmin, vmax)

    if ok:
        return value

    return None

def popup_get_color(base_color: QColor, text: str, window) -> QColor:
    color = QColorDialog.getColor(base_color, window, text)

    if color.isValid():
        return color

    return None
