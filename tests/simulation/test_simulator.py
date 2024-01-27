# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

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


def test_simulator_from_cli_arguments(monkeypatch):
    args = Mock(
        field_size=(100, 200),
        traveler_collider_radius=5,
        hornet_velocity_range=(1, 3),
        hornet_collider_radius=2,
        hornet_count=5,
    )
    mock_traveler = Mock(spec=Agent)
    mock_hornets = [Mock(spec=Agent) for _ in range(args.hornet_count)]
    monkeypatch.setattr("simulation.simulator._create_traveler", Mock(return_value=mock_traveler))
    monkeypatch.setattr("simulation.simulator._create_hornets", Mock(return_value=mock_hornets))

    simulator = Simulator.from_cli_arguments(args)

    assert isinstance(simulator, Simulator)
    assert simulator.traveler is mock_traveler
    assert simulator.hornets == mock_hornets
    assert len(simulator.hornets) == args.hornet_count


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
