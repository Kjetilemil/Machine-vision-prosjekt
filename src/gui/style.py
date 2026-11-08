from PyQt6.QtWidgets import QApplication

# each theme is just a set of colors, the stylesheet below uses them
THEMES = {
    "dark": {
        "window": "#1e1f22",      # menu bar, status bar and dialogs
        "canvas": "#121316",      # the area behind the image
        "surface": "#2b2d31",     # menus and input fields
        "border": "#3a3c42",
        "text": "#e6e6e6",
        "muted": "#9a9ca3",       # less important text, like the status bar
        "accent": "#4c8dff",      # hover and selected items
        "accent_text": "#ffffff",
        "accent_soft": "rgba(76, 141, 255, 40)",
    },
    "light": {
        "window": "#ffffff",
        "canvas": "#eef0f3",
        "surface": "#ffffff",
        "border": "#dcdfe4",
        "text": "#1f2329",
        "muted": "#6b7280",
        "accent": "#2f6fed",
        "accent_text": "#ffffff",
    },
    "midnight": {
        "window": "#161a2b",
        "canvas": "#0d1020",
        "surface": "#20263d",
        "border": "#2e3554",
        "text": "#e8eaf6",
        "muted": "#8f96b8",
        "accent": "#8b5cf6",
        "accent_text": "#ffffff",
    },
}


def build_stylesheet(colors):
    """Turns a set of colors into a Qt stylesheet (works like CSS for Qt widgets)."""
    return f"""
        QWidget {{
            background-color: {colors["window"]};
            color: {colors["text"]};
            font-size: 13px;
        }}

        /* the area behind the image */
        QStackedWidget, ZoomableLabel {{
            background-color: {colors["canvas"]};
        }}

        QMenuBar {{
            background-color: {colors["window"]};
            border-bottom: 1px solid {colors["border"]};
            padding: 4px 6px;
        }}
        QMenuBar::item {{
            background: transparent;
            padding: 6px 12px;
            border-radius: 6px;
        }}
        QMenuBar::item:selected {{
            background-color: {colors["surface"]};
        }}

        QMenu {{
            background-color: {colors["surface"]};
            border: 1px solid {colors["border"]};
            border-radius: 8px;
            padding: 6px;
        }}
        QMenu::item {{
            padding: 7px 28px 7px 14px;
            border-radius: 5px;
        }}
        QMenu::item:selected {{
            background-color: {colors["accent"]};
            color: {colors["accent_text"]};
        }}
        QMenu::separator {{
            height: 1px;
            background: {colors["border"]};
            margin: 5px 8px;
        }}

        QStatusBar {{
            background-color: {colors["window"]};
            border-top: 1px solid {colors["border"]};
            color: {colors["muted"]};
            padding: 2px 8px;
        }}

        QPushButton {{
            background-color: {colors["surface"]};
            border: 1px solid {colors["border"]};
            border-radius: 6px;
            padding: 6px 16px;
        }}
        QPushButton:hover {{
            border-color: {colors["accent"]};
        }}

        /* the big button on the start screen */
        QPushButton#openButton {{
            background-color: {colors["accent"]};
            color: {colors["accent_text"]};
            border: none;
            border-radius: 10px;
            font-size: 16px;
            padding: 14px 40px;
        }}
        QPushButton#openButton:hover {{
            background-color: {colors["accent"]};
            padding: 15px 42px;
        }}

                /* the chosen tool, in the right corner of the status bar */
        QLabel#toolChip {{
            background-color: {colors["accent_soft"]};
            color: {colors["accent"]};
            border-radius: 9px;
            padding: 2px 10px;
            margin: 2px 4px;
            font-weight: 600;
        }}

        QLabel#title {{
            background: transparent;
            font-size: 28px;
            font-weight: 600;
        }}
        QLabel#subtitle {{
            background: transparent;
            color: {colors["muted"]};
            font-size: 14px;
        }}

        QLineEdit, QSpinBox {{
            background-color: {colors["surface"]};
            border: 1px solid {colors["border"]};
            border-radius: 6px;
            padding: 5px 8px;
            selection-background-color: {colors["accent"]};
        }}
        QLineEdit:focus, QSpinBox:focus {{
            border-color: {colors["accent"]};
        }}

        QToolTip {{
            background-color: {colors["surface"]};
            color: {colors["text"]};
            border: 1px solid {colors["border"]};
            padding: 4px 8px;
        }}
    """


def apply_theme(app: QApplication, theme="dark"):
    app.setStyle("Fusion")
    app.setStyleSheet(build_stylesheet(THEMES[theme]))