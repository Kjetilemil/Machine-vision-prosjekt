import cv2
import numpy as np

def open_image(img_path):
    image = cv2.imread(img_path)

    if image is None:
        raise ValueError("Could not load the image")

    else:
        return image

def save_image(path: str, img: np.ndarray) -> None:
    if not img:
        return

    cv2.imwrite(path, img)
