"""Entry point for the Hornet Field"""

import argparse
import os
import shutil
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
        "--max-iteration",
        default=float("inf"),
        type=float,
        help="Maximum iteration count, after which the process will terminate",
    )
    parser.add_argument(
        "--save-to-file",
        action="store_true",
        help="Save frames as images.",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        type=str,
        help="Path to directory to save images.",
    )
    return parser.parse_args(argv)


def _prepare_output_dir(dir_path: str):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)


def main(argv: Sequence[str]):
    # pylint: disable=missing-function-docstring
    args = _parse_arguments(argv)

    if args.save_to_file:
        if args.max_iteration == float("inf"):
            raise ValueError("--max-iteration must be set if --save-to-file is true")
        _prepare_output_dir(args.output_dir)

    simulator = Simulator.from_cli_arguments(args)
    visualizer = Visualizer.from_cli_arguments(args)

    iteration = 1
    while True:
        simulator.tick()
        hud_texts = [
            f"Iteration: {iteration:>{6}} / {args.max_iteration}",
            f"Time (ms): {visualizer.time_ms:>{6}}",
            f"Run count: {simulator.traveler_run_count:>{6}}",
        ]
        visualizer.tick(simulator, hud_texts)
        if args.save_to_file:
            visualizer.save_to_file(os.path.join(args.output_dir, f"frame_{iteration:05}.png"))
        if pygame_quit() or iteration > args.max_iteration:
            break
        iteration += 1

    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
