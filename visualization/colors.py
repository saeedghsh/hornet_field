"""Colors and helpers"""

from typing import Tuple

Color = Tuple[int, int, int]

COLORS = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
}


def lighten_color(color: Color, ratio: float = 0.5) -> Color:
    """Return a lighter version of the same color
    ratio=1 makes the color WHITE
    ratio=0 does not change the color"""
    return tuple(int(v + ratio * (255 - v)) for v in color)  # type: ignore


def darken_color(color: Color, ratio: float = 0.5) -> Color:
    """Return a darker version of the same color
    ratio=1 makes the color BLACK
    ratio=0 does not change the color"""
    return tuple(int(v - ratio * v) for v in color)  # type: ignore
