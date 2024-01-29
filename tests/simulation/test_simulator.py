# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

import argparse
import copy
from itertools import chain

import pytest

from simulation.agents import Agent, Collider, Pose, Position, Velocity
from simulation.simulator import Simulator


@pytest.mark.parametrize("hornet_count", [0, 1, 10])
def test_simulator_initialization(hornet_count: int):
    traveler = Agent(Pose(Position(0, 0)), Velocity(0, 0), Collider(0))
    hornets = [
        Agent(Pose(Position(0, 0)), Velocity(0, 0), Collider(0)) for _ in range(hornet_count)
    ]
    field_size = (10, 10)
    simulator = Simulator(traveler, hornets, field_size)
    assert simulator.traveler is traveler
    assert simulator.hornets is hornets
    assert len(simulator.hornets) == hornet_count


def test_simulator_tick():
    # given
    traveler = Agent(Pose(Position(0, 0)), Velocity(1, 0), Collider(0))
    traveler_former_position = copy.copy(traveler.pose.position)
    hornets = [Agent(Pose(Position(0, 0)), Velocity(1, 0), Collider(0))]
    hornets_former_position = [copy.copy(hornet.pose.position) for hornet in hornets]
    field_size = (10, 10)
    simulator = Simulator(traveler, hornets, field_size)
    # when
    simulator.tick()
    # then: pose.position should be changed
    assert traveler_former_position != traveler.pose.position
    for idx, hornet in enumerate(hornets):
        assert hornets_former_position[idx] != hornet.pose.position


def test_simulator_collision_count():
    traveler = Agent(Pose(Position(5, 5)), Velocity(0, 0), Collider(1))
    hornets = [Agent(Pose(Position(1, 1)), Velocity(0, 0), Collider(1)) for _ in range(3)]
    field_size = (10, 10)
    simulator = Simulator(traveler, hornets, field_size)

    simulator.tick()
    assert simulator.collision_count == 0

    # hornets[0] just collided
    simulator.hornets[0].pose.position = Position(5, 5)
    simulator.tick()
    assert simulator.collision_count == 1

    # hornets[1] just collided, # hornets[0] and hornets[2] not in collision
    simulator.hornets[0].pose.position = Position(1, 1)
    simulator.hornets[1].pose.position = Position(5, 5)
    simulator.tick()
    assert simulator.collision_count == 2

    # hornets[1] already in collision
    # hornets[0] and hornets[2] just collided
    simulator.hornets[0].pose.position = Position(5, 5)
    simulator.hornets[2].pose.position = Position(5, 5)
    simulator.tick()
    assert simulator.collision_count == 4


def test_simulator_traveler_run_count():
    traveler = Agent(Pose(Position(9, 5)), Velocity(2, 0), Collider(0))
    hornets = []
    field_size = (10, 10)
    simulator = Simulator(traveler, hornets, field_size)
    former_count = copy.copy(simulator.traveler_run_count)
    simulator.tick()
    assert simulator.traveler_run_count == former_count + 1


def test_simulator_collision():
    traveler = Agent(Pose(Position(0, 0)), Velocity(1, 0), Collider(1))
    hornets = [Agent(Pose(Position(0, 0)), Velocity(1, 0), Collider(1))]
    field_size = (10, 10)
    simulator = Simulator(traveler, hornets, field_size)
    assert simulator.collision()
    traveler.pose.position = Position(5, 5)
    assert not simulator.collision()


def test_do_collide():
    agents = {
        1: Agent(Pose(Position(0, 0)), Velocity(0, 0), Collider(1)),
        2: Agent(Pose(Position(1, 1)), Velocity(0, 0), Collider(1)),
        3: Agent(Pose(Position(-10, 0)), Velocity(0, 0), Collider(10)),
        4: Agent(Pose(Position(10, 10)), Velocity(0, 0), Collider(1)),
    }
    collisions = [(1, 2), (1, 3)]
    colliding_agent_indices = list(chain(*collisions))
    all_indices = list(agents.keys())
    for self_idx in all_indices:
        simulator = Simulator(
            traveler=agents[self_idx],
            hornets=[agents[other_idx] for other_idx in all_indices if other_idx != self_idx],
            field_size=(100, 100),
        )

        if self_idx in colliding_agent_indices:
            assert simulator.collision()
        else:
            assert not simulator.collision()


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
