import cv2


def add_text(image, text, position, color, size):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, text, position, font, size, color, 2, cv2.LINE_AA)
    return image

