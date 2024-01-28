"""Entry point for the Hornet Field"""

import argparse
from dataclasses import dataclass
from typing import Sequence

import pygame

from simulation.agents import Agent, Cartesian
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


@dataclass
class HeadsUpDisplayConfig:
    # pylint: disable=missing-class-docstring
    text_origin: Cartesian = Cartesian(2, 2)
    text_line_gap: int = 0
    font_size: int = 15
    font_color: Color = COLORS["white"]
    font_face: str = pygame.font.match_font("Courier")  # any monospaced font


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
        self._hud_config = HeadsUpDisplayConfig()
        self._hud_font = pygame.font.Font(self._hud_config.font_face, self._hud_config.font_size)

    @staticmethod
    def from_cli_arguments(args: argparse.Namespace) -> "Visualizer":
        config = VisualizerConfig(
            surface_color=lighten_color(COLORS[args.field_color]),
            hornet_color=COLORS[args.hornet_color],
            traveler_color=COLORS[args.traveler_color],
            traveler_collision_color=COLORS[args.traveler_collision_color],
            frame_rate=args.frame_rate,
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

    def _hud_overlay(self, hud_texts: Sequence[str]):
        for idx, line in enumerate(hud_texts):
            x = self._hud_config.text_origin.x
            y = self._hud_config.text_origin.y
            y += idx * (self._hud_config.font_size + self._hud_config.text_line_gap)
            text_surface = self._hud_font.render(line, True, self._hud_config.font_color, None)
            self._surface.blit(text_surface, (x, y))

    def tick(self, simulator: Simulator, hud_texts: Sequence[str]):
        if simulator.collision():
            traveler_color = self._config.traveler_collision_color
        else:
            traveler_color = self._config.traveler_color
        self._surface.fill(self._config.surface_color)
        agents = [simulator.traveler] + simulator.hornets
        colors = [traveler_color] + len(simulator.hornets) * [self._config.hornet_color]
        for agent, color in zip(agents, colors):
            self._draw_agent(agent, color)
        self._hud_overlay(hud_texts)
        pygame.display.flip()
        self._clock.tick(self._config.frame_rate)

    def save_to_file(self, file_path: str):
        pygame.image.save(self._surface, file_path)


def pygame_quit() -> bool:
    """Return True if a pygame.QUIT event occurred.
    pygame.QUIT: e.g. when user closes the display window."""
    # pylint: disable=no-member
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return True
    return False
