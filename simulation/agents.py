"""Agent (traveler and hornet)"""

# pylint: disable=missing-class-docstring
import logging
from dataclasses import dataclass
from typing import Any, Tuple

import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class Cartesian:
    x: float
    y: float

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Cartesian):
            return np.isclose(self.as_list(), other.as_list()).all().astype(bool)
        return NotImplemented

    def as_list(self) -> list:  # pylint: disable=missing-function-docstring
        return [self.x, self.y]

    def as_ndarray(self) -> np.ndarray:  # pylint: disable=missing-function-docstring
        return np.array(self.as_list())


@dataclass(eq=False)
class Position(Cartesian):
    @staticmethod
    def random_position(size: Tuple[int, int]) -> "Position":
        """Return a random position bound to [0, width] and [0, height]"""
        width, height = size
        if width <= 0 or height <= 0:
            error_message = f"Size must be positive value; got {size}"
            logger.error(error_message)
            raise ValueError(error_message)
        return Position(np.random.randint(0, width), np.random.randint(0, height))


@dataclass
class Velocity(Cartesian):
    @staticmethod
    def random_velocity(_range: Tuple[float, float]) -> "Velocity":
        """Return a random velocity bound to _range = [_min, _max]"""
        _min, _max = _range
        if _min >= _max:
            error_message = f"Min must be less than max; got {_range}"
            logger.error(error_message)
            raise ValueError(error_message)
        interval = _max - _min
        return Velocity(np.random.rand() * interval + _min, np.random.rand() * interval + _min)


@dataclass
class Pose:
    position: Position


@dataclass
class Collider:
    radius: float

    def __post_init__(self):
        if self.radius < 0:
            error_message = f"Collider radius cannot be negative, got: {self.radius}"
            logger.error(error_message)
            raise ValueError(error_message)


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

    def _distance(self, other: "Agent") -> float:  # pragma: no cover
        return np.linalg.norm(
            self.pose.position.as_ndarray() - other.pose.position.as_ndarray()
        ).astype(float)

    def does_collide(self, other: "Agent") -> bool:
        """Return True if self collides with the other"""
        if self._distance(other) < self.collider.radius + other.collider.radius:
            return True
        return False
