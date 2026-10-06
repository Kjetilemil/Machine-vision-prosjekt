from controller.file_controller import open_image, save_image

class Controller:
    def __init__(self, window):
        self.window = window
        self.current_img = None

    def open_image(self):
        open_image(self)

    def save_image_as(self):
        save_image(self)
