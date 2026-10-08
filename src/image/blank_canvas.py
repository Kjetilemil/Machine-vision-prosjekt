import numpy as np


def create_blank_canvas(width, height, color):
    width = int(width)
    height = int(height)

    return np.full((height, width, 3), color, dtype=np.uint8)


# TODO: Add functionality to allow user to specify width, height, and color of the blank canvas? 
def run_blank_canvas():
    canvas = create_blank_canvas(800, 600, (255, 255, 255)) 
    return canvas