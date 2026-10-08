import cv2


def rotate_right(image):
    rotated_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    return rotated_image

def rotate_left(image):
    rotated_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return rotated_image

def flip_horizontal(image):
    flipped_image = cv2.flip(image, 1)
    return flipped_image

def flip_vertical(image):
    flipped_image = cv2.flip(image, 0)
    return flipped_image


