"""Entry point for the Hornet Field"""

import argparse
import sys
from typing import Sequence

from simulation.simulator import Simulator
from visualization.colors import available_colors
from visualization.visualizer import Visualizer, pygame_quit

COLOR_CHOICES = available_colors()


def _parse_arguments(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Hornet Field entry point")
    parser.add_argument(
        "--hornet-count",
        type=int,
        default=200,
        help="Number of hornet agents in the field.",
    )
    parser.add_argument(
        "--hornet-color",
        default="yellow",
        choices=COLOR_CHOICES,
        type=str,
        help="The color of hornet agent.",
    )
    parser.add_argument(
        "--hornet-collider-radius",
        default=5.0,
        type=float,
        help="The radius of the collider of hornet agent.",
    )
    parser.add_argument(
        "--hornet-velocity-range",
        default=(-5.0, 5.0),
        nargs=2,
        type=float,
        help="The range from which random velocity for hornet agent are drawn.",
    )
    parser.add_argument(
        "--traveler-color",
        default="blue",
        choices=COLOR_CHOICES,
        type=str,
        help="The color of traveler agent.",
    )
    parser.add_argument(
        "--traveler-collider-radius",
        default=20.0,
        type=float,
        help="The radius of the collider of traveler agent.",
    )
    parser.add_argument(
        "--traveler-collision-color",
        default="red",
        choices=COLOR_CHOICES,
        type=str,
        help="The color of traveler agent with in collision.",
    )
    parser.add_argument(
        "--field-color",
        default="black",
        choices=COLOR_CHOICES,
        type=str,
        help="The color of field (selected color will be lightened e.g. black -> gray).",
    )
    parser.add_argument(
        "--field-size",
        default=(2400, 1200),
        nargs=2,
        type=int,
        help="The size (width, height) of the field.",
    )
    parser.add_argument(
        "--frame-rate",
        default=200,
        type=float,
        help="The frame rate (fps).",
    )
    parser.add_argument(
        "--collision-frame-rate",
        default=50,
        type=float,
        help="The frame rate (fps) during collision. Used to slow animation during collision",
    )
    parser.add_argument(
        "--max-iteration",
        default=float("inf"),
        type=float,
        help="Maximum iteration count, after which the process will terminate",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str]):
    # pylint: disable=missing-function-docstring
    args = _parse_arguments(argv)
    simulator = Simulator.from_cli_arguments(args)
    visualizer = Visualizer.from_cli_arguments(args)

    iteration = 0
    while True:
        simulator.tick()
        visualizer.tick(simulator)
        if pygame_quit() or iteration > args.max_iteration:
            break
        iteration += 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
