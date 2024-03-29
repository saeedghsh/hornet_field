# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
import argparse
import os
from unittest.mock import Mock, patch

import pytest

from simulation.agents import Agent, Collider, Pose, Position, Velocity
from simulation.simulator import Simulator
from visualization.colors import COLORS
from visualization.visualizer import Visualizer, VisualizerConfig, pygame_quit


def test_visualizer_config_initialization():
    # given
    expected_surface_color = (255, 0, 0)
    expected_hornet_color = (0, 255, 0)
    expected_traveler_color = (0, 0, 255)
    expected_traveler_collision_color = (255, 255, 0)
    expected_frame_rate = 60.0
    # when
    actual_config = VisualizerConfig(
        surface_color=expected_surface_color,
        hornet_color=expected_hornet_color,
        traveler_color=expected_traveler_color,
        traveler_collision_color=expected_traveler_collision_color,
        frame_rate=expected_frame_rate,
    )
    # then
    assert actual_config.surface_color == expected_surface_color
    assert actual_config.hornet_color == expected_hornet_color
    assert actual_config.traveler_color == expected_traveler_color
    assert actual_config.traveler_collision_color == expected_traveler_collision_color
    assert actual_config.frame_rate == expected_frame_rate


@patch("visualization.visualizer.pygame")
def test_pygame_quit(pygame_mock):
    mock_event = Mock()
    mock_event.type = pygame_mock.QUIT
    pygame_mock.event.get.return_value = [mock_event]

    assert pygame_quit() is True
    pygame_mock.event.get.return_value = []
    assert pygame_quit() is False


@patch("visualization.visualizer.pygame")
def test_visualizer_from_cli_arguments(pygame_mock):
    # given
    args = Mock(
        field_size=(100, 200),
        field_color="green",
        hornet_color="red",
        traveler_color="blue",
        traveler_collision_color="yellow",
        frame_rate=60.0,
    )
    # when
    visualizer = Visualizer.from_cli_arguments(args)
    # then
    assert isinstance(visualizer, Visualizer)
    pygame_mock.init.assert_called()
    pygame_mock.display.set_mode.assert_called_with(args.field_size)
    pygame_mock.display.set_caption.assert_called_with("Hornet Field Simulation")


@patch("visualization.visualizer.pygame")
def test_visualizer_tick(pygame_mock):
    config = VisualizerConfig(
        surface_color=COLORS["green"],
        hornet_color=COLORS["red"],
        traveler_color=COLORS["blue"],
        traveler_collision_color=COLORS["yellow"],
        frame_rate=60.0,
    )
    traveler = Agent(Pose(Position(0, 0)), Velocity(0, 0), Collider(0))
    hornet = Agent(Pose(Position(1, 1)), Velocity(0, 0), Collider(0))
    simulator = Simulator(traveler, 3 * [hornet], (10, 10))
    visualizer = Visualizer(surface_size=(100, 200), config=config)
    hud_texts = [""]
    visualizer.tick(simulator, hud_texts)
    pygame_mock.display.flip.assert_called()
    assert pygame_mock.draw.circle.call_count == 2 * 4  # 1 traveler + 3 hornets (twice per agent)


def test_visualizer_tick_smoke_test():
    args = argparse.Namespace(
        hornet_count=1,
        hornet_color="yellow",
        hornet_collider_radius=1,
        hornet_velocity_range=(0, 1),
        traveler_color="blue",
        traveler_collider_radius=1,
        traveler_collision_color="red",
        field_color="green",
        field_size=(10, 10),
        frame_rate=60.0,
    )
    hud_texts = [""]
    simulator = Simulator.from_cli_arguments(args)
    visualizer = Visualizer.from_cli_arguments(args)
    simulator.traveler.velocity.x = 0
    simulator.traveler.velocity.y = 0
    simulator.traveler.pose.position.x = 0
    simulator.traveler.pose.position.y = 1
    simulator.hornets[0].pose.position.x = 3
    simulator.hornets[0].pose.position.y = 5
    simulator.hornets[0].velocity.x = 0
    simulator.hornets[0].velocity.y = 0
    assert not simulator.collision()
    visualizer.tick(simulator, hud_texts)
    simulator.traveler.pose.position.x = simulator.hornets[0].pose.position.x
    simulator.traveler.pose.position.y = simulator.hornets[0].pose.position.y
    assert simulator.collision()
    visualizer.tick(simulator, hud_texts)


def test_visualizer_save_to_file_smoke_test(tmp_path: str):
    args = argparse.Namespace(
        hornet_count=1,
        hornet_color="yellow",
        hornet_collider_radius=1,
        hornet_velocity_range=(0, 1),
        traveler_color="blue",
        traveler_collider_radius=1,
        traveler_collision_color="red",
        field_color="green",
        field_size=(10, 10),
        frame_rate=60.0,
    )
    hud_texts = [""]
    simulator = Simulator.from_cli_arguments(args)
    visualizer = Visualizer.from_cli_arguments(args)
    visualizer.tick(simulator, hud_texts)
    file_path = os.path.join(tmp_path, "tmp.png")
    visualizer.save_to_file(file_path)
    assert os.path.exists(file_path)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
