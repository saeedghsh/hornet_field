# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import pytest

from visualization.colors import available_colors, darken_color, lighten_color


def test_available_colors():
    expected_colors = ["black", "red", "green", "blue", "yellow", "white"]
    assert sorted(available_colors()) == sorted(expected_colors)


def test_lighten_color():
    assert lighten_color((100, 100, 100), 0.5) == (177, 177, 177)
    assert lighten_color((100, 100, 100), 0) == (100, 100, 100)
    assert lighten_color((100, 100, 100), 1) == (255, 255, 255)


def test_darken_color():
    assert darken_color((100, 100, 100), 0.5) == (50, 50, 50)
    assert darken_color((100, 100, 100), 0) == (100, 100, 100)
    assert darken_color((100, 100, 100), 1) == (0, 0, 0)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
