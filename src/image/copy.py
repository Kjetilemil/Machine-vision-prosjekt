import numpy as np


def copy_image(image):
    height, width, channels = image.shape
    copied_image = np.zeros((height, width, 3), dtype=np.uint8)
    copied_image[:] = image[:]
    return copied_image