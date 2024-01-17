"""Entry point for the Hornet Field"""

import argparse
import sys
from typing import Sequence

import pygame

from agents import Agent, Collider, Pose, Position, Velocity, do_collide
from colors import COLORS, Color, darken_color, lighten_color


def _pygame_quit(events) -> bool:
    for event in events:
        if event.type == pygame.QUIT:  # pylint: disable=no-member
            return True
    return False


def _draw_agent(surface: pygame.Surface, agent: Agent, color: Color):
    pygame.draw.circle(
        surface=surface,
        color=lighten_color(color),
        center=agent.pose.position.as_list(),
        radius=agent.collider.radius,
    )
    pygame.draw.circle(
        surface=surface,
        color=darken_color(color),
        center=agent.pose.position.as_list(),
        radius=1,
    )


def _update_field_surface(
    surface: pygame.Surface,
    surface_color: Color,
    agents: Sequence[Agent],
    colors: Sequence[Color],
):
    surface.fill(surface_color)
    for agent, color in zip(agents, colors):
        _draw_agent(surface, agent, color)


def _parse_arguments(argv: Sequence[str]):
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
        type=int,
        help="The frame rate (fps).",
    )
    parser.add_argument(
        "--collision-frame-rate",
        default=50,
        type=int,
        help="The frame rate (fps) during collision. Used to slow animation during collision",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str]):
    # pylint: disable=missing-function-docstring
    args = _parse_arguments(argv)

    field_color = lighten_color(COLORS[args.field_color])
    hornet_color = COLORS[args.hornet_color]

    traveler = Agent(
        Pose(Position(0, args.field_size[1] // 2)),
        Velocity(2, 0),
        Collider(args.traveler_collider_radius),
    )
    hornets = [
        Agent(
            pose=Pose(Position.random_position(args.field_size)),
            velocity=Velocity.random_velocity(args.hornet_velocity_range),
            collider=Collider(args.hornet_collider_radius),
        )
        for i in range(args.hornet_count)
    ]

    pygame.init()  # pylint: disable=no-member
    screen = pygame.display.set_mode(args.field_size)
    pygame.display.set_caption("Hornet Simulation")
    clock = pygame.time.Clock()

    while True:
        if _pygame_quit(pygame.event.get()):
            break

        # move the agents
        traveler.update(args.field_size)
        for hornet in hornets:
            hornet.update(args.field_size)

        # detect collision
        if do_collide(traveler, hornets):
            traveler_color = COLORS[args.traveler_collision_color]
            frame_rate = args.collision_frame_rate
        else:
            traveler_color = COLORS[args.traveler_color]
            frame_rate = args.frame_rate

        _update_field_surface(
            surface=screen,
            surface_color=field_color,
            agents=[traveler] + hornets,
            colors=[traveler_color] + args.hornet_count * [hornet_color],
        )

        pygame.display.flip()
        clock.tick(frame_rate)

    pygame.quit()  # pylint: disable=no-member


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
