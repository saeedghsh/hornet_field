"""Entry point for the Hornet Field"""

import argparse
from dataclasses import dataclass
from typing import Sequence

import pygame

from simulation.agents import Agent
from simulation.simulator import Simulator
from visualization.colors import COLORS, Color, darken_color, lighten_color


@dataclass
class VisualizerConfig:
    # pylint: disable=missing-class-docstring
    surface_color: Color
    hornet_color: Color
    traveler_color: Color
    traveler_collision_color: Color
    frame_rate: float
    collision_frame_rate: float


class Visualizer:
    # pylint: disable=missing-class-docstring
    # pylint: disable=missing-function-docstring
    # pylint: disable=no-member
    def __init__(self, surface_size: Sequence[int], config: VisualizerConfig):
        self._config = config
        pygame.init()
        self._surface = pygame.display.set_mode(surface_size)
        pygame.display.set_caption("Hornet Field Simulation")
        self._clock = pygame.time.Clock()

    @staticmethod
    def from_cli_arguments(args: argparse.Namespace) -> "Visualizer":
        config = VisualizerConfig(
            surface_color=lighten_color(COLORS[args.field_color]),
            hornet_color=COLORS[args.hornet_color],
            traveler_color=COLORS[args.traveler_color],
            traveler_collision_color=COLORS[args.traveler_collision_color],
            frame_rate=args.frame_rate,
            collision_frame_rate=args.collision_frame_rate,
        )
        return Visualizer(surface_size=args.field_size, config=config)

    def _draw_agent(self, agent: Agent, color: Color):
        pygame.draw.circle(
            surface=self._surface,
            color=lighten_color(color),
            center=agent.pose.position.as_list(),
            radius=agent.collider.radius,
        )
        pygame.draw.circle(
            surface=self._surface,
            color=darken_color(color),
            center=agent.pose.position.as_list(),
            radius=1,
        )

    def _update(self, agents: Sequence[Agent], colors: Sequence[Color], frame_rate: float):
        self._surface.fill(self._config.surface_color)
        for agent, color in zip(agents, colors):
            self._draw_agent(agent, color)
        pygame.display.flip()
        self._clock.tick(frame_rate)

    def tick(self, simulator: Simulator):
        if simulator.collision():
            traveler_color = self._config.traveler_collision_color
            frame_rate = self._config.collision_frame_rate
        else:
            traveler_color = self._config.traveler_color
            frame_rate = self._config.frame_rate
        hornet_colors = len(simulator.hornets) * [self._config.hornet_color]
        self._update(
            agents=[simulator.traveler] + simulator.hornets,
            colors=[traveler_color] + hornet_colors,
            frame_rate=frame_rate,
        )


def pygame_quit() -> bool:
    """Return True if a pygame.QUIT event occurred.
    pygame.QUIT: e.g. when user closes the display window."""
    # pylint: disable=no-member
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False
