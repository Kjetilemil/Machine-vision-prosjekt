ZOOM_STEP = 1.25
MIN_ZOOM = 0.1
MAX_ZOOM = 5.0


def zoom_in(current_zoom):
    return min(round(current_zoom * ZOOM_STEP, 2), MAX_ZOOM)


def zoom_out(current_zoom):
    return max(round(current_zoom / ZOOM_STEP, 2), MIN_ZOOM)