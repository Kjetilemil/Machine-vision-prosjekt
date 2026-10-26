from PyQt6.QtWidgets import QInputDialog

def popup_get_integer(default: int, vmin: int, vmax: int, text: str, window) -> int:
    value, ok = QInputDialog.getInt(window, "Input", text, default, vmin, vmax)

    if ok:
        return value

    return None
