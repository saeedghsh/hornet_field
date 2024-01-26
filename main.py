"""Entry point for the Hornet Field"""

import argparse
import sys
from typing import List, Sequence

from simulation.agents import Agent, Collider, Pose, Position, Velocity, do_collide
from visualization.colors import COLORS, lighten_color
from visualization.drawing import initialize_drawing, pygame_quit, update_drawing


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
        choices=list(COLORS.keys()),
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
        choices=list(COLORS.keys()),
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
        choices=list(COLORS.keys()),
        type=str,
        help="The color of traveler agent with in collision.",
    )
    parser.add_argument(
        "--field-color",
        default="green",
        choices=list(COLORS.keys()),
        type=str,
        help="The color of field.",
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
    return parser.parse_args(argv)


def _create_traveler(args: argparse.Namespace) -> Agent:
    return Agent(
        Pose(Position(0, args.field_size[1] // 2)),
        Velocity(2, 0),
        Collider(args.traveler_collider_radius),
    )


def _create_hornets(args: argparse.Namespace) -> List[Agent]:
    return [
        Agent(
            pose=Pose(Position.random_position(args.field_size)),
            velocity=Velocity.random_velocity(args.hornet_velocity_range),
            collider=Collider(args.hornet_collider_radius),
        )
        for i in range(args.hornet_count)
    ]


def main(argv: Sequence[str]):
    # pylint: disable=missing-function-docstring
    args = _parse_arguments(argv)

    traveler = _create_traveler(args)
    hornets = _create_hornets(args)
    drawing = initialize_drawing(args.field_size, "Hornet Simulation")
    surface = drawing["surface"]
    clock = drawing["clock"]
    field_color = lighten_color(COLORS[args.field_color])
    hornet_colors = args.hornet_count * [COLORS[args.hornet_color]]

    while True:
        # tick: simulation
        for agent in [traveler] + hornets:
            agent.update(args.field_size)
        collision = do_collide(traveler, hornets)

        # tick: drawing
        if collision:
            traveler_color = COLORS[args.traveler_collision_color]
            frame_rate = args.collision_frame_rate
        else:
            traveler_color = COLORS[args.traveler_color]
            frame_rate = args.frame_rate
        update_drawing(
            surface=surface,
            surface_color=field_color,
            agents=[traveler] + hornets,
            colors=[traveler_color] + hornet_colors,
            clock=clock,
            frame_rate=frame_rate,
        )

        # handle quitting
        if pygame_quit():
            break


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
