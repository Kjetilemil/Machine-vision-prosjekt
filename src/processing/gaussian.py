import cv2
import numpy as np
from processing.constants import DEFAULT_GAUSSIAN_KERNEL_SIZE


def apply_gaussian_filter(
    image: np.ndarray,
    kernel_size: int = DEFAULT_GAUSSIAN_KERNEL_SIZE,
) -> np.ndarray:
    if image is None:
        raise ValueError("No image available")

    if kernel_size <= 0 or kernel_size % 2 == 0:
        raise ValueError("kernel_size must be a positive odd integer")

    return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
