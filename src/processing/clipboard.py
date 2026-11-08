import cv2
import numpy as np

# cut leaves a white hole, like the eraser
CUT_COLOR = (255, 255, 255)  # white in BGR
FRAME_COLOR = (0, 255, 255)  # yellow in BGR, the same as the selections


def rectangle_mask(image, top_left, bottom_right):
    """Makes a mask where the rectangle is 255 and the rest is 0, so it works like the other selections."""
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    x0, y0 = top_left
    x1, y1 = bottom_right
    mask[y0:y1, x0:x1] = 255
    return mask


def copy_area(image, mask):
    """Cuts out the smallest rectangle around the selection.
    Returns the piece and its mask, so a free-form or polygon selection keeps its own form when pasted."""
    x, y, width, height = cv2.boundingRect(mask)
    piece = image[y:y + height, x:x + width].copy()
    piece_mask = mask[y:y + height, x:x + width].copy()
    return piece, piece_mask


def cut_area(image, mask):
    """Returns a copy of the image where the selection is white."""
    result = image.copy()
    result[mask > 0] = CUT_COLOR
    return result


def paste_area(image, piece, piece_mask, position):
    """Pastes the piece with its top left corner at position (x, y), the position can also be outside the image.
    Only the pixels inside piece_mask are pasted, the parts outside the image are left out."""
    result = image.copy()
    x, y = position
    image_height, image_width = image.shape[:2]
    piece_height, piece_width = piece.shape[:2]

    # the part of the image that the piece covers
    left = max(x, 0)
    top = max(y, 0)
    right = min(x + piece_width, image_width)
    bottom = min(y + piece_height, image_height)
    if right <= left or bottom <= top:
        return result

    target = result[top:bottom, left:right]
    piece_part = piece[top - y:bottom - y, left - x:right - x]
    inside = piece_mask[top - y:bottom - y, left - x:right - x] > 0
    target[inside] = piece_part[inside]
    return result


def keep_piece_on_image(image, piece, position):
    """Moves the position so at least a part of the piece stays on the image and can still be grabbed."""
    image_height, image_width = image.shape[:2]
    piece_height, piece_width = piece.shape[:2]
    x = min(max(position[0], 1 - piece_width), image_width - 1)
    y = min(max(position[1], 1 - piece_height), image_height - 1)
    return x, y


def is_on_piece(piece, position, point):
    """True if the point (x, y) is inside the box of the piece at position."""
    piece_height, piece_width = piece.shape[:2]
    return (
        position[0] <= point[0] < position[0] + piece_width
        and position[1] <= point[1] < position[1] + piece_height
    )


def draw_paste_frame(image, piece, position):
    """Returns a copy of the image with a yellow frame around the pasted piece, so the user sees what can be moved."""
    preview = image.copy()
    piece_height, piece_width = piece.shape[:2]
    thickness = max(2, max(image.shape[:2]) // 400)  # thicker line on big images so it can be seen
    x, y = position
    cv2.rectangle(preview, (x, y), (x + piece_width - 1, y + piece_height - 1), FRAME_COLOR, thickness)
    return preview


def selection_position(mask):
    """The top left corner (x, y) of the selection, this is where a paste goes."""
    x, y, _, _ = cv2.boundingRect(mask)
    return x, y
