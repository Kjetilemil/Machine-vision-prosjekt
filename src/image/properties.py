



# gets height, width and channels of an image
def get_image_properties(image):
    height, width, channels = image.shape
    return height, width, channels


def get_pixel_color(image, x, y):
    blue, green, red = image[y, x]
    return blue, green, red
    