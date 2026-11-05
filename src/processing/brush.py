import cv2


def paint_line(image, start, end, color, size):
    """Paints a round line from start to end. Painting from a point to itself makes a dot."""
    cv2.line(image, start, end, color, size, cv2.LINE_AA)
    return image
