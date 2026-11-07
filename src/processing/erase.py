from processing.brush import paint_line

# the images have no transparency, so erasing paints in the background color like in Paint
ERASE_COLOR = (255, 255, 255)  # white in BGR


def erase_line(image, start, end, size):
    """Erases a round line from start to end. Erasing from a point to itself erases a dot."""
    return paint_line(image, start, end, ERASE_COLOR, size)
