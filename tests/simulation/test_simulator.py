# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import argparse
from unittest.mock import Mock, create_autospec

import pytest

from simulation.agents import Agent
from simulation.simulator import Simulator


def test_simulator_initialization():
    traveler = Mock(spec=Agent)
    hornets = [Mock(spec=Agent) for _ in range(3)]
    field_size = (100, 200)
    simulator = Simulator(traveler, hornets, field_size)
    assert simulator.traveler is traveler
    assert simulator.hornets is hornets
    assert len(simulator.hornets) == 3


def test_simulator_tick():
    traveler = create_autospec(Agent)
    hornets = [create_autospec(Agent) for _ in range(3)]
    field_size = (100, 200)
    simulator = Simulator(traveler, hornets, field_size)
    simulator.tick()
    traveler.update.assert_called_once_with(field_size)
    for hornet in hornets:
        hornet.update.assert_called_once_with(field_size)


def test_simulator_collision(monkeypatch):
    traveler = Mock(spec=Agent)
    hornets = [Mock(spec=Agent) for _ in range(3)]
    field_size = (100, 200)
    simulator = Simulator(traveler, hornets, field_size)
    monkeypatch.setattr("simulation.agents.do_collide", Mock(return_value=True))
    assert simulator.collision() is True


def test_simulator_from_cli_arguments():
    # given
    args = argparse.Namespace(
        field_size=(100, 200),
        hornet_count=5,
        hornet_velocity_range=(1, 3),
        hornet_collider_radius=2,
        traveler_collider_radius=5,
    )
    # when
    simulator = Simulator.from_cli_arguments(args)
    # then
    assert isinstance(simulator, Simulator)
    assert simulator.traveler.pose.position.x == 0
    assert simulator.traveler.pose.position.y == args.field_size[1] // 2
    assert simulator.traveler.collider.radius == args.traveler_collider_radius
    assert len(simulator.hornets) == args.hornet_count
    field_width, field_height = args.field_size
    vel_min, vel_max = args.hornet_velocity_range
    for hornet in simulator.hornets:
        assert hornet.collider.radius == args.hornet_collider_radius
        assert 0 <= hornet.pose.position.x <= field_width
        assert 0 <= hornet.pose.position.y <= field_height
        assert vel_min <= hornet.velocity.x <= vel_max
        assert vel_min <= hornet.velocity.y <= vel_max


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
