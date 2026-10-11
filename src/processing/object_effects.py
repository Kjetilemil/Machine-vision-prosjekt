import cv2
import numpy as np

from processing.constants import DEFAULT_OBJECT_BLUR_KERNEL_SIZE, DEFAULT_HUE_SHIFT


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


def shift_object_color(
    image: np.ndarray,
    mask: np.ndarray,
    hue_shift: int = DEFAULT_HUE_SHIFT,
) -> np.ndarray:
    """Changes the color (hue) of the selected object. The rest of the image stays the same."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # hue goes from 0 to 179 in OpenCV, so we wrap around with % 180
    hue = hsv[:, :, 0].astype(np.int32)
    hsv[:, :, 0] = ((hue + hue_shift) % 180).astype(np.uint8)
    shifted = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    result = image.copy()
    result[mask > 0] = shifted[mask > 0]
    return result
