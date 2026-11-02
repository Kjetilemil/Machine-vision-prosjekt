import cv2



def rectangle_selection(image, start_point, end_point, color, thickness):
    cv2.rectangle(image, start_point, end_point, color, thickness)
    return image