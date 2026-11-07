import cv2
import numpy as np

SELECTION_COLOR = (0, 255, 255)  # yellow in BGR, the same as the rectangle selection


def polygon_mask(image, points):
    """Makes a mask where everything inside the points is 255 and the rest is 0.
    Used by both free-form (many points) and polygon (a few corners)."""
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    corners = np.array(points, dtype=np.int32)
    cv2.fillPoly(mask, [corners], 255)
    return mask


def draw_selection_line(image, points, closed=False):
    """Returns a copy of the image with a yellow line through the points, the image itself is not changed."""
    preview = image.copy()
    thickness = max(2, max(image.shape[:2]) // 400)  # thicker line on big images so it can be seen
    corners = np.array(points, dtype=np.int32)
    cv2.polylines(preview, [corners], closed, SELECTION_COLOR, thickness, cv2.LINE_AA)
    return preview


def is_close_to(point, other_point, image):
    """True if the two points are so close that the user most likely meant the same point."""
    max_distance = max(10, max(image.shape[:2]) // 60)  # grows with the image, so it is easy to hit
    dx = point[0] - other_point[0]
    dy = point[1] - other_point[1]
    return dx * dx + dy * dy <= max_distance * max_distance