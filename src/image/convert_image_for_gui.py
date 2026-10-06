import cv2
from PyQt6.QtGui import QImage, QPixmap


# converts the OpenCV format of the selected image for gui
def convert_opencv_to_gui_image(opencv_image):
    converted_image = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB)

    height, width, channel = converted_image.shape
    bytes = channel * width

    gui_image = QImage(
        converted_image.data,
        width,
        height,
        bytes,
        QImage.Format.Format_RGB888
    )

    draw_image = QPixmap.fromImage(gui_image)
    return draw_image
