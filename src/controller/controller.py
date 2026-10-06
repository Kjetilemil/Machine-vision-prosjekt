from controller.file_controller import handle_open_image

class Controller:
    def __init__(self, window):
        self.window = window

    def open_file_system(self):
        handle_open_image(self.window)
