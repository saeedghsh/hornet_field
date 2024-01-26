"""Entry point for the Hornet Field"""

from typing import Sequence, TypedDict

import pygame

from agents import Agent
from colors import Color, darken_color, lighten_color


class Drawing(TypedDict, total=True):
    # pylint: disable=missing-class-docstring
    surface: pygame.Surface
    clock: pygame.time.Clock


def initialize_drawing(surface_size: Sequence[int], title: str) -> Drawing:
    """Initialize drawing with pygame.
    Create and return surface and clock
    """
    # pylint: disable=no-member
    pygame.init()
    surface = pygame.display.set_mode(surface_size)
    pygame.display.set_caption(title)
    clock = pygame.time.Clock()
    return Drawing({"surface": surface, "clock": clock})


def pygame_quit() -> bool:
    """Quit pygame and Return True if a pygame.QUIT event occurs.
    pygame.QUIT: e.g. when user closes the display window."""
    # pylint: disable=no-member
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
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


def update_drawing(
    surface: pygame.Surface,
    surface_color: Color,
    agents: Sequence[Agent],
    colors: Sequence[Color],
    clock: pygame.time.Clock,
    frame_rate: float,
):
    """Update the drawings on the surface."""
    # pylint: disable=too-many-arguments
    surface.fill(surface_color)
    for agent, color in zip(agents, colors):
        _draw_agent(surface, agent, color)
    pygame.display.flip()
    clock.tick(frame_rate)
