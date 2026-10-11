from PyQt6.QtWidgets import QMainWindow
from controller.controller import Controller
from gui.menubar import add_menu_action


# row of buttons under the menu bar for the most used actions
def create_toolbar(window: QMainWindow, controller: Controller):
    toolbar = window.addToolBar("Toolbar")
    toolbar.setMovable(False)

    add_menu_action(toolbar, "Open", controller.open_image)
    add_menu_action(toolbar, "Save", controller.save_image)
    toolbar.addSeparator()

    # the shortcuts are set in the Edit menu, so they are not added here
    add_menu_action(toolbar, "Undo", controller.undo)
    add_menu_action(toolbar, "Redo", controller.redo)
    toolbar.addSeparator()

    add_menu_action(toolbar, "Select object", controller.select_object_tool)
    add_menu_action(toolbar, "Blur object", controller.blur_selected_object)
    add_menu_action(toolbar, "Change color", controller.shift_selected_object_color)
    add_menu_action(toolbar, "Remove object", controller.remove_selected_object)
