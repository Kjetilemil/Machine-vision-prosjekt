import cv2
import numpy as np

from processing.constants import DEFAULT_OBJECT_BLUR_KERNEL_SIZE


def blur_object(
    image: np.ndarray,
    mask: np.ndarray,
    kernel_size: int = DEFAULT_OBJECT_BLUR_KERNEL_SIZE,
) -> np.ndarray:
    """Blurs only the selected object. The rest of the image stays the same."""
    if kernel_size <= 0 or kernel_size % 2 == 0:
        raise ValueError("kernel_size must be a positive odd integer")

    # blur the whole image, then keep the blurred pixels only where the object is
    blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    result = image.copy()
    result[mask > 0] = blurred[mask > 0]
    return result


def recolor_object(
    image: np.ndarray,
    mask: np.ndarray,
    color: tuple,
) -> np.ndarray:
    """Gives the selected object a new color (B, G, R). The light and shadows on the object are kept."""
    # LAB splits a color into lightness (L) and the color itself (a and b)
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    new_lab = cv2.cvtColor(np.uint8([[color]]), cv2.COLOR_BGR2LAB)[0, 0]

    # take the color (a and b) from the new color, but keep the lightness from the image
    # so the light, shadows and shine on the object are still there
    lab[:, :, 1] = new_lab[1]
    lab[:, :, 2] = new_lab[2]
    recolored = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    result = image.copy()
    result[mask > 0] = recolored[mask > 0]
    return result
