import cv2
import numpy as np

def filesystem_open_image(img_path):
    image = cv2.imread(img_path)

    if image is None:
        raise ValueError("Could not load the image")

    else:
        return image

def filesystem_save_image(path: str, img: np.ndarray) -> None:
    if img is None:
        return

    try:
        saved = cv2.imwrite(path, img)
    except cv2.error as error:
        raise ValueError(f"Could not save the image: {error}") from error

    if not saved:
        raise ValueError("Could not save the image")
