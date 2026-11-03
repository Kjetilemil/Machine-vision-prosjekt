import cv2
import numpy as np

from processing.constants import DEFAULT_SHAPE_OUTLINE_THICKNESS


def _regular_polygon(corners, rotation=-90):
    """Points of a regular polygon inside a 1x1 box. rotation=-90 puts the first corner at the top."""
    angles = np.radians(rotation + np.arange(corners) * 360 / corners)
    return [(0.5 + 0.5 * np.cos(a), 0.5 + 0.5 * np.sin(a)) for a in angles]


def _star(points=5, inner_ratio=0.4):
    """Points of a star inside a 1x1 box, going between the outer and the inner corners."""
    star = []
    for i in range(points * 2):
        radius = 0.5 if i % 2 == 0 else 0.5 * inner_ratio
        angle = np.radians(-90 + i * 180 / points)
        star.append((0.5 + radius * np.cos(angle), 0.5 + radius * np.sin(angle)))
    return star


# every polygon shape is described inside a 1x1 box, (0, 0) is the top left and (1, 1) the bottom right
# the points are scaled to the box the user clicks, so a new shape only needs a new entry here
POLYGON_SHAPES = {
    "Rectangle": [(0, 0), (1, 0), (1, 1), (0, 1)],
    "Square": [(0, 0), (1, 0), (1, 1), (0, 1)],
    "Triangle": [(0.5, 0), (1, 1), (0, 1)],
    "Right triangle": [(0, 0), (1, 1), (0, 1)],
    "Diamond": [(0.5, 0), (1, 0.5), (0.5, 1), (0, 0.5)],
    "Parallelogram": [(0.25, 0), (1, 0), (0.75, 1), (0, 1)],
    "Trapezoid": [(0.25, 0), (0.75, 0), (1, 1), (0, 1)],
    "Pentagon": _regular_polygon(5),
    "Hexagon": _regular_polygon(6, rotation=0),
    "Octagon": _regular_polygon(8, rotation=22.5),
    "Star": _star(),
    "Cross": [
        (1 / 3, 0), (2 / 3, 0), (2 / 3, 1 / 3), (1, 1 / 3), (1, 2 / 3), (2 / 3, 2 / 3),
        (2 / 3, 1), (1 / 3, 1), (1 / 3, 2 / 3), (0, 2 / 3), (0, 1 / 3), (1 / 3, 1 / 3),
    ],
}

# the arrow goes from the start to the end point, so it is described along its own direction:
# (along, across), along goes from 0 (start) to 1 (tip), across is the distance from the middle
ARROW_POINTS = [(0, -0.1), (0.65, -0.1), (0.65, -0.25), (1, 0), (0.65, 0.25), (0.65, 0.1), (0, 0.1)]

# shapes that keep the same width and height, no matter how the user clicks
EQUAL_SIDE_SHAPES = ["Square", "Circle"]

# shapes that go from the start to the end point instead of filling the box between them
DIRECTION_SHAPES = ["Line", "Arrow"]

SHAPES = list(POLYGON_SHAPES) + ["Circle", "Ellipse", "Arrow", "Line"]


def _make_sides_equal(start, end):
    """Moves the end point so the box becomes a square, in the direction the user clicked."""
    x1, y1 = start
    x2, y2 = end
    side = min(abs(x2 - x1), abs(y2 - y1))
    x2 = x1 + side if x2 >= x1 else x1 - side
    y2 = y1 + side if y2 >= y1 else y1 - side
    return (x2, y2)


def _snap_line(start, end):
    """Moves the end point so the line goes in steps of 45 degrees (straight, or exactly diagonal)."""
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    angle = np.round(np.arctan2(dy, dx) / (np.pi / 4)) * (np.pi / 4)
    length = np.hypot(dx, dy)
    return (int(round(start[0] + length * np.cos(angle))), int(round(start[1] + length * np.sin(angle))))


def constrain_end(shape, start, end, keep_proportions=False):
    """The end point the shape is really drawn to. keep_proportions is used when Shift is held."""
    if shape in DIRECTION_SHAPES:
        return _snap_line(start, end) if keep_proportions else end
    if keep_proportions or shape in EQUAL_SIDE_SHAPES:
        return _make_sides_equal(start, end)
    return end


def is_too_small(shape, start, end):
    """True when the mouse barely moved, then nothing should be drawn."""
    width = abs(end[0] - start[0])
    height = abs(end[1] - start[1])
    if shape in DIRECTION_SHAPES:
        return max(width, height) < 2
    return width < 2 or height < 2


def draw_shape(
    image: np.ndarray,
    shape: str,
    start: tuple,
    end: tuple,
    fill_color: tuple,
    outline_color: tuple,
    thickness: int = DEFAULT_SHAPE_OUTLINE_THICKNESS,
    keep_proportions: bool = False,
) -> np.ndarray:
    """Draws the shape in the box between start and end (x, y). The colors are in BGR."""
    if shape not in SHAPES:
        raise ValueError(f"Unknown shape: {shape}")

    result = image.copy()
    end = constrain_end(shape, start, end, keep_proportions)

    left, right = sorted((start[0], end[0]))
    top, bottom = sorted((start[1], end[1]))
    width = right - left
    height = bottom - top

    # a line has no inside, so it only gets the outline color
    if shape == "Line":
        cv2.line(result, start, end, outline_color, thickness, cv2.LINE_AA)
        return result

    if shape in ("Circle", "Ellipse"):
        center = (left + width // 2, top + height // 2)
        axes = (width // 2, height // 2)
        cv2.ellipse(result, center, axes, 0, 0, 360, fill_color, -1, cv2.LINE_AA)
        cv2.ellipse(result, center, axes, 0, 0, 360, outline_color, thickness, cv2.LINE_AA)
        return result

    if shape == "Arrow":
        # the direction from start to end, and the direction across it, both scaled to the arrow length
        along = np.array(end, dtype=np.float64) - start
        across = np.array([-along[1], along[0]])
        points = np.array(
            [start + a * along + c * across for a, c in ARROW_POINTS],
            dtype=np.int32,
        )
    else:
        # scale the points from the 1x1 box to the box the user clicked
        points = np.array(
            [(left + x * width, top + y * height) for x, y in POLYGON_SHAPES[shape]],
            dtype=np.int32,
        )
    cv2.fillPoly(result, [points], fill_color, cv2.LINE_AA)
    cv2.polylines(result, [points], True, outline_color, thickness, cv2.LINE_AA)
    return result
