import cv2



def open_image(img_path):
    image = cv2.imread(img_path)

    if image is None:
        raise ValueError("Could not load the image")

    else: 
        return image


