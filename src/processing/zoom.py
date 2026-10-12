ZOOM_STEP = 1.25
MIN_ZOOM = 0.1
MAX_ZOOM = 5.0


def zoom_in(current_zoom):
    return min(round(current_zoom * ZOOM_STEP, 2), MAX_ZOOM)


def zoom_out(current_zoom):
    return max(round(current_zoom / ZOOM_STEP, 2), MIN_ZOOM)


# used by pinch on the trackpad, factor is a small change like 1.02 or 0.98
def zoom_by(current_zoom, factor):
    return min(max(current_zoom * factor, MIN_ZOOM), MAX_ZOOM)
