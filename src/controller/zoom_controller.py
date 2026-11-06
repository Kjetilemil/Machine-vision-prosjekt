from processing.zoom import zoom_in as calculate_zoom_in, zoom_out as calculate_zoom_out
from processing.zoom import zoom_by as calculate_zoom_by


def run_zoom_in(controller):
        run_start_zoom_preview(controller, calculate_zoom_in)


# zooms in one step right away, used by the keyboard shortcut
def run_zoom_in_directly(controller):
        if controller.current_img is None:
            return

        controller.zoom_factor = calculate_zoom_in(controller.zoom_factor)
        controller.window.set_zoom_factor(controller.zoom_factor)


# zooms with pinch on the trackpad
def run_zoom_by(controller, factor):
        if controller.current_img is None:
            return

        controller.zoom_factor = calculate_zoom_by(controller.zoom_factor, factor)
        controller.window.set_zoom_factor(controller.zoom_factor)


def run_zoom_out(controller):
        if controller.current_img is None:
            return

        controller.zoom_factor = calculate_zoom_out(controller.zoom_factor)
        controller.window.set_zoom_factor(controller.zoom_factor)


def run_start_zoom_preview(controller, calculate_zoom):
        if controller.current_img is None:
            return

        next_zoom = calculate_zoom(controller.zoom_factor)
        controller.window.start_zoom_preview(
            next_zoom,
            lambda image_x, image_y, view_x, view_y: run_apply_zoom(
                controller, next_zoom, image_x, image_y, view_x, view_y
            ),
        )


def run_apply_zoom(controller, zoom_factor, image_x, image_y, view_x, view_y):
        controller.zoom_factor = zoom_factor
        controller.window.set_zoom_factor(zoom_factor, image_x, image_y, view_x, view_y)

