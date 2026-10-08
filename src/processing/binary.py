import cv2
import numpy as np

from processing.constants import DEFAULT_BINARY_THRESHOLD


def apply_binary_filter(
    image: np.ndarray,
    threshold: int = DEFAULT_BINARY_THRESHOLD,
) -> np.ndarray:
    if image is None:
        raise ValueError("No image available")

    if threshold < 0 or threshold > 255:
        raise ValueError("threshold must be between 0 and 255")

    if image.ndim == 2:
        gray = image
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
