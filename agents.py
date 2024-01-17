"""Agent (traveler and hornet)"""

# pylint: disable=missing-class-docstring
import random
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np


@dataclass
class Cartesian:
    x: float
    y: float

    def as_list(self) -> list:  # pylint: disable=missing-function-docstring
        return [self.x, self.y]

    def as_ndarray(self) -> np.ndarray:  # pylint: disable=missing-function-docstring
        return np.array(self.as_list())


@dataclass
class Position(Cartesian):
    @staticmethod
    def random_position(size: Tuple[int, int]) -> "Position":
        """Return a random position bound to [0, width] and [0, height]"""
        width, height = size
        return Position(random.randint(0, width), random.randint(0, height))


@dataclass
class Velocity(Cartesian):
    @staticmethod
    def random_velocity(_range: Tuple[float, float]) -> "Velocity":
        """Return a random velocity bound to _range = [_min, _max]"""
        _min, _max = _range
        if _min >= _max:
            raise ValueError(f"Min must be less than max; got {_range}")
        interval = _max - _min
        return Velocity(random.random() * interval + _min, random.random() * interval + _min)


@dataclass
class Pose:
    position: Position


@dataclass
class Collider:
    radius: float


@dataclass
class Agent:
    pose: Pose
    velocity: Velocity
    collider: Collider

    def update(self, field_size: Tuple[int, int]):
        """Update self.pose according to self.velocity

        NOTE: self.velocity is also updated to keep the agent inside the field."""
        self.pose.position.x += self.velocity.x
        self.pose.position.y += self.velocity.y
        width, height = field_size
        if not 0 <= self.pose.position.x <= width:
            self.velocity.x *= -1
        if not 0 <= self.pose.position.y <= height:
            self.velocity.y *= -1

    def _distance(self, other: "Agent") -> float:
        return np.linalg.norm(
            self.pose.position.as_ndarray() - other.pose.position.as_ndarray()
        ).astype(float)

    def does_collide(self, other: "Agent") -> bool:
        """Return True if self collides with the other"""
        if self._distance(other) < self.collider.radius + other.collider.radius:
            return True
        return False


def do_collide(agent: Agent, others: List[Agent]) -> bool:
    """Return True if agent collides with any of the others"""
    for other in others:
        if agent.does_collide(other):
            return True
    return False
