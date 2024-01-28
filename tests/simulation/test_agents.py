# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from itertools import chain, combinations
from typing import List, Tuple

import numpy as np
import pytest

from simulation.agents import Agent, Cartesian, Collider, Pose, Position, Velocity, do_collide


@pytest.mark.parametrize(
    "point1, point2, equality",
    [
        [Cartesian(3.0, 4.0), Cartesian(3.0, 4.0), True],
        [Cartesian(-3.0, 4.0), Cartesian(3.0, 4.0), False],
        [Cartesian(-3.0, 4.0), Cartesian(-3.0, 4.0), True],
    ],
)
def test_cartesian_eq(point1: Cartesian, point2: Cartesian, equality: bool):
    assert (point1 == point2) == equality


def test_cartesian_eq_not_implemented():
    # pylint: disable=unnecessary-dunder-call
    assert Cartesian(0.0, 0.0).__eq__([0, 0]) is NotImplemented


@pytest.mark.parametrize("expected_point", [[3.0, 4.0], [-3.0, 4.0], [100.0, -10.0]])
def test_cartesian_as_list(expected_point: List[float]):
    actual_point = Cartesian(*expected_point)
    actual_result = actual_point.as_list()
    assert isinstance(actual_result, list)
    assert actual_result == expected_point


@pytest.mark.parametrize("expected_point", [[3.0, 4.0], [-3.0, 4.0], [100.0, -10.0]])
def test_cartesian_as_ndarray(expected_point: List[float]):
    actual_point = Cartesian(*expected_point)
    actual_result = actual_point.as_ndarray()
    assert isinstance(actual_result, np.ndarray)
    assert np.array_equal(actual_result, np.array(expected_point))


@pytest.mark.parametrize("expected_size", [(3, 4), (40, 30), (100, 1111)])
def test_position_random_position(expected_size: Tuple[int, int]):
    actual_position = Position.random_position(expected_size)
    assert isinstance(actual_position, Position)
    assert 0 <= actual_position.x <= expected_size[0]
    assert 0 <= actual_position.y <= expected_size[1]


@pytest.mark.parametrize("expected_size", [(-3, 4), (40, -30), (-100, -1111)])
def test_position_random_position_invalid_size(expected_size: Tuple[int, int]):
    with pytest.raises(ValueError):
        Position.random_position(expected_size)


@pytest.mark.parametrize("expected_range", [(-3.0, 4.0), (4.0, 30.0), (-100.0, 0.0)])
def test_velocity_random_velocity(expected_range: Tuple[float, float]):
    actual_velocity = Velocity.random_velocity(expected_range)
    assert isinstance(actual_velocity, Velocity)
    assert expected_range[0] <= actual_velocity.x <= expected_range[1]
    assert expected_range[0] <= actual_velocity.y <= expected_range[1]


@pytest.mark.parametrize("expected_range", [(3.0, -4.0), (4.0, 0.0), (-100.0, -100.01)])
def test_velocity_random_velocity_invalid_range(expected_range: Tuple[float, float]):
    with pytest.raises(ValueError):
        Velocity.random_velocity(expected_range)


@pytest.mark.parametrize("expected_point", [[3.0, 4.0], [-3.0, 4.0], [100.0, -10.0]])
def test_pose_initialization(expected_point: List[float]):
    actual_pose = Pose(Position(*expected_point))
    assert actual_pose.position.as_list() == expected_point


@pytest.mark.parametrize("expected_radius", [3.0, 4.0, 100.0, 10.0, 0.0])
def test_collider_initialization(expected_radius: float):
    actual_collider = Collider(expected_radius)
    assert actual_collider.radius == expected_radius


@pytest.mark.parametrize("expected_radius", [-3.0, -4.0, -10.0])
def test_collider_initialization_invalid_radius(expected_radius: float):
    with pytest.raises(ValueError):
        Collider(expected_radius)


@pytest.mark.parametrize("position", [[9, 5], [6.5, 10], [1, 1]])
@pytest.mark.parametrize("velocity", [[1, 1], [2.5, -1.0]])
@pytest.mark.parametrize("field_size", [(50, 50), (10, 10)])
def test_agent_update(position: List[float], velocity: List[float], field_size: Tuple[int, int]):
    expected_position = [
        position[0] + velocity[0],
        position[1] + velocity[1],
    ]
    expected_velocity = [
        velocity[0] if 0 <= expected_position[0] <= field_size[0] else -velocity[0],
        velocity[1] if 0 <= expected_position[1] <= field_size[1] else -velocity[1],
    ]
    actual_agent = Agent(Pose(Position(*position)), Velocity(*velocity), Collider(0))
    actual_agent.update(field_size)
    assert actual_agent.pose.position.x == expected_position[0]
    assert actual_agent.pose.position.y == expected_position[1]
    assert actual_agent.velocity.x == expected_velocity[0]
    assert actual_agent.velocity.y == expected_velocity[1]


def _collision_test_data():
    agents = {
        1: Agent(Pose(Position(0, 0)), Velocity(0, 0), Collider(1)),
        2: Agent(Pose(Position(1, 1)), Velocity(0, 0), Collider(1)),
        3: Agent(Pose(Position(-10, 0)), Velocity(0, 0), Collider(10)),
        4: Agent(Pose(Position(10, 10)), Velocity(0, 0), Collider(1)),
    }
    collisions = [(1, 2), (1, 3)]
    return agents, collisions


def test_agent_does_collide():
    agents, collisions = _collision_test_data()
    for idx1, idx2 in list(combinations(agents.keys(), 2)):
        if (idx1, idx2) in collisions:
            assert agents[idx1].does_collide(agents[idx2])
            assert agents[idx2].does_collide(agents[idx1])
        else:
            assert not agents[idx1].does_collide(agents[idx2])
            assert not agents[idx2].does_collide(agents[idx1])


def test_do_collide():
    agents, collisions = _collision_test_data()
    colliding_agent_indices = list(chain(*collisions))
    all_indices = list(agents.keys())
    for self_idx in all_indices:
        self_agent = agents[self_idx]
        other_agents = [agents[other_idx] for other_idx in all_indices if other_idx != self_idx]
        if self_idx in colliding_agent_indices:
            assert do_collide(self_agent, other_agents)
        else:
            assert not do_collide(self_agent, other_agents)


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))
