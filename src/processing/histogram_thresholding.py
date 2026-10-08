import cv2
import numpy as np


def apply_histogram_thresholding(image: np.ndarray) -> np.ndarray:
    if image is None:
        raise ValueError("No image available")

    if image.ndim == 2:
        gray = image
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
