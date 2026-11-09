




import cv2


def crop(image, x_0, x_1, y_0, y_1):
    cropped_image = image[y_0:y_1, x_0:x_1]
    return cropped_image


# crops to the smallest rectangle around the selection (255 = selected).
# for a free-form, polygon or object selection the corners around the shape are kept, like in Paint
def crop_to_mask(image, mask):
    x, y, width, height = cv2.boundingRect(mask)
    return crop(image, x, x + width, y, y + height)


