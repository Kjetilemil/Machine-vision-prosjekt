import cv2
import numpy as np

# GrabCut is slow on big images, so we work on a smaller copy
MAX_SIZE = 600

# how much to blur when splitting the image into a smooth part and a detail part
DETAIL_BLUR_SIGMA = 3


def select_object(image, x, y):
    """Finds the object at pixel (x, y). Returns a mask where 255 = object and 0 = background."""
    height, width = image.shape[:2]

    # 1. make a smaller copy of the image so it runs fast
    scale = min(1.0, MAX_SIZE / max(height, width))
    small = cv2.resize(image, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    small_h, small_w = small.shape[:2]
    sx = min(int(x * scale), small_w - 1)
    sy = min(int(y * scale), small_h - 1)

    # 2. flood fill from the click to get a rough guess of the object
    flood = np.zeros((small_h + 2, small_w + 2), np.uint8)
    tolerance = (12, 12, 12)
    flags = 4 | cv2.FLOODFILL_MASK_ONLY | cv2.FLOODFILL_FIXED_RANGE | (255 << 8)
    cv2.floodFill(small.copy(), flood, (sx, sy), 0, tolerance, tolerance, flags)
    rough = flood[1:-1, 1:-1]

    # 3. tell GrabCut what we know, and let it find the real edges
    mask = np.full((small_h, small_w), cv2.GC_PR_BGD, np.uint8)  # probably background
    mask[rough > 0] = cv2.GC_PR_FGD                              # probably object
    cv2.circle(mask, (sx, sy), 5, cv2.GC_FGD, -1)                # the click is surely object

    background_model = np.zeros((1, 65), np.float64)
    foreground_model = np.zeros((1, 65), np.float64)
    cv2.grabCut(small, mask, None, background_model, foreground_model, 5, cv2.GC_INIT_WITH_MASK)
    object_mask = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)

    # 4. keep only the part that is connected to the click, then scale back up
    _, labels = cv2.connectedComponents(object_mask)
    if labels[sy, sx] == 0:
        return np.zeros((height, width), np.uint8)  # nothing found
    object_mask = np.where(labels == labels[sy, sx], 255, 0).astype(np.uint8)
    # scale back up smoothly so the edges are not blocky, then make it black/white again
    object_mask = cv2.resize(object_mask, (width, height), interpolation=cv2.INTER_LINEAR)
    return np.where(object_mask > 127, 255, 0).astype(np.uint8)

def draw_selection(image, mask):
    """Returns a copy of the image with the selected object tinted blue and outlined in yellow."""
    preview = image.copy()

    # light blue tint on the object
    tint = np.full_like(image, (255, 200, 0))  # light blue in BGR
    tinted = cv2.addWeighted(image, 0.7, tint, 0.3, 0)
    preview[mask > 0] = tinted[mask > 0]

    # yellow outline around the object
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    thickness = max(2, max(image.shape[:2]) // 300)  # thicker line on bigger images
    cv2.drawContours(preview, contours, -1, (0, 255, 255), thickness)  # yellow in BGR
    return preview

def remove_object(image, mask):
    """Removes the object and fills the hole with generated background (inpainting)."""
    # the mask was made on a smaller copy, so one small pixel can be many pixels here.
    # grow the mask by about 3 small pixels (at least 9x9) so no edge pixels are left behind
    height, width = mask.shape[:2]
    scale = max(1.0, max(height, width) / MAX_SIZE)
    size = max(9, int(3 * scale) | 1)  # | 1 makes it odd
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (size, size))
    bigger_mask = cv2.dilate(mask, kernel)
    filled = cv2.inpaint(image, bigger_mask, 5, cv2.INPAINT_TELEA)
    return add_texture(image, filled, bigger_mask, kernel)

def add_texture(image, filled, mask, kernel):
    """Inpainting makes the hole smooth. This adds back texture (like skin pores) that matches the area around it."""
    # frequency separation: the details are what is left when we remove the smooth (blurred) part
    smooth = cv2.GaussianBlur(image, (0, 0), DETAIL_BLUR_SIGMA)
    details = image.astype(np.float32) - smooth

    # measure how strong the details are in a ring around the hole.
    # skip the area right next to the hole, the blur smears the object's edge into it
    near = cv2.dilate(mask, kernel)
    ring = cv2.dilate(near, kernel) - near
    if not ring.any():
        return filled
    strength = details[ring > 0].std(axis=0)  # one value per color channel

    # random noise with the same strength, same for all channels so it changes brightness, not color
    height, width = mask.shape[:2]
    noise = np.random.default_rng().normal(0, 1, (height, width, 1)) * strength

    result = filled.copy()
    textured = np.clip(filled + noise, 0, 255).astype(np.uint8)
    result[mask > 0] = textured[mask > 0]
    return result