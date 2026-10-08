import cv2
import numpy as np

from processing.constants import DEFAULT_SOBEL_KERNEL_SIZE


def apply_sobel_filter(
    image: np.ndarray,
    kernel_size: int = DEFAULT_SOBEL_KERNEL_SIZE,
) -> np.ndarray:
    if image is None:
        raise ValueError("No image available")

    if kernel_size <= 0 or kernel_size % 2 == 0:
        raise ValueError("kernel_size must be a positive odd integer")

    if image.ndim == 2:
        gray = image
    else:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=kernel_size)
    sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=kernel_size)
    magnitude = cv2.magnitude(sobel_x, sobel_y)
    edges = cv2.convertScaleAbs(magnitude)

    return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
