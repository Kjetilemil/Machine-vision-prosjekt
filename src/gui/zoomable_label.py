from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPainter, QPen
from PyQt6.QtWidgets import QLabel


class ZoomableLabel(QLabel):
    image_clicked = pyqtSignal(int, int)
    def __init__(self, parent=None):
        
        super().__init__(parent)
        self._source_image = None
        self._zoom_factor = 1.0
        self._focus_image = (0.5, 0.5)
        self._focus_view = (0.5, 0.5)
        self._preview_zoom = None
        self._preview_position = None
        self._zoom_callback = None
        
        

    def set_image(self, image):
        self._source_image = image
        self.update()

    def set_zoom(self, zoom_factor, image_x=None, image_y=None, view_x=None, view_y=None):
        self._zoom_factor = zoom_factor
        if image_x is not None:
            self._focus_image = (image_x, image_y)
            self._focus_view = (view_x, view_y)
        self.update()

    def start_zoom_preview(self, zoom_factor, callback):
        self._preview_zoom = zoom_factor
        self._zoom_callback = callback
        self._preview_position = None
        self.setMouseTracking(True)
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.update()

    def _finish_zoom_preview(self):
        self._preview_zoom = None
        self._preview_position = None
        self._zoom_callback = None
        self.setMouseTracking(False)
        self.unsetCursor()

    def _image_rect(self, zoom_factor, focus_image, focus_view):
        fitted_image = self._source_image.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        scaled_image = fitted_image.scaled(
            max(1, round(fitted_image.width() * zoom_factor)),
            max(1, round(fitted_image.height() * zoom_factor)),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        focus_x = round(self.width() * focus_view[0])
        focus_y = round(self.height() * focus_view[1])
        image_x = self._image_offset(
            self.width(), scaled_image.width(), focus_x, focus_image[0]
        )
        image_y = self._image_offset(
            self.height(), scaled_image.height(), focus_y, focus_image[1]
        )
        return scaled_image, scaled_image.rect().translated(image_x, image_y)

    @staticmethod
    def _image_offset(view_size, image_size, focus_position, focus_ratio):
        if image_size <= view_size:
            return (view_size - image_size) // 2

        desired_offset = round(focus_position - focus_ratio * image_size)
        return max(view_size - image_size, min(0, desired_offset))

    def _preview_focus(self, position):
        _, current_rect = self._image_rect(
            self._zoom_factor, self._focus_image, self._focus_view
        )
        if not current_rect.contains(position):
            return None

        image_x = (position.x() - current_rect.x()) / current_rect.width()
        image_y = (position.y() - current_rect.y()) / current_rect.height()
        view_x = position.x() / self.width()
        view_y = position.y() / self.height()
        return (image_x, image_y), (view_x, view_y)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self._source_image is None or self.width() <= 0 or self.height() <= 0:
            return

        zoom_factor = self._zoom_factor
        focus_image = self._focus_image
        focus_view = self._focus_view
        preview_focus = None
        if self._preview_zoom is not None and self._preview_position is not None:
            preview_focus = self._preview_focus(self._preview_position)
            if preview_focus is not None:
                zoom_factor = self._preview_zoom
                focus_image, focus_view = preview_focus

        scaled_image, image_rect = self._image_rect(
            zoom_factor, focus_image, focus_view
        )
        painter = QPainter(self)
        painter.drawPixmap(image_rect.topLeft(), scaled_image)
        if preview_focus is not None:
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(QPen(Qt.GlobalColor.black, 3))
            painter.drawEllipse(self._preview_position, 6, 6)
            painter.setPen(QPen(Qt.GlobalColor.white, 1))
            painter.drawEllipse(self._preview_position, 6, 6)

    def mouseMoveEvent(self, event):
        if self._preview_zoom is not None:
            self._preview_position = event.position().toPoint()
            self.update()
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mousePressEvent(self, event):
        if (
            self._zoom_callback is not None
            and event.button() == Qt.MouseButton.LeftButton
        ):
            position = event.position().toPoint()
            focus = self._preview_focus(position)
            if focus is not None:
                callback = self._zoom_callback
                image_focus, view_focus = focus
                self._finish_zoom_preview()
                callback(*image_focus, *view_focus)
                event.accept()
                return

        # checks where the user clicked on the image and emits a signal with the coordinates
        if self._source_image is not None:
            click = self._preview_focus(event.position().toPoint())
            if click is not None:
                image_position, window_position = click
                x_part, y_part = image_position
                x = int(x_part * self._source_image.width())
                y = int(y_part * self._source_image.height())
                self.image_clicked.emit(x, y)

        super().mousePressEvent(event)