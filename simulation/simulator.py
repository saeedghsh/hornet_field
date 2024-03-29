"""Entry point for the Hornet Field"""

import argparse
import copy
import logging
from typing import List, Sequence

from simulation.agents import Agent, Collider, Pose, Position, Velocity

logger = logging.getLogger(__name__)


class Simulator:
    # pylint: disable=missing-class-docstring
    # pylint: disable=missing-function-docstring
    def __init__(self, traveler: Agent, hornets: List[Agent], field_size: Sequence[int]):
        self._traveler = traveler
        self._hornets = hornets
        self._field_size = field_size
        self._traveler_run_count = 0
        self._colliding_hornets_idx: List[int] = []  # those in collision with traveler
        self._collision_count = 0  # count of total [unique] hornet-traveler collision
        self._iteration = 0

        logger.info("Created simulator")
        logger.info("Simulator has a of size: %d x %d", *field_size)
        logger.info("Simulator has %d traveler(s)", 1)
        logger.info("Simulator has %d hornets(s)", len(hornets))

    def tick(self):
        former_velocity = copy.copy(self._traveler.velocity)
        self._traveler.update(self._field_size)
        bounced = former_velocity != self._traveler.velocity
        if bounced:
            self._traveler_run_count += 1

        former_indices = set(self._colliding_hornets_idx)
        for hornet in self._hornets:
            hornet.update(self._field_size)
        if self.collision():
            new_colliding_idx = set(self._colliding_hornets_idx) - former_indices
            self._collision_count += len(new_colliding_idx)
        self._iteration += 1

    def _update_collision_list(self):  # pragma: no cover
        self._colliding_hornets_idx = [
            idx for idx, hornet in enumerate(self._hornets) if self._traveler.does_collide(hornet)
        ]

    def collision(self) -> bool:
        self._update_collision_list()
        return len(self._colliding_hornets_idx) != 0

    @property
    def iteration(self) -> int:
        return self._iteration

    @property
    def collision_count(self) -> int:
        return self._collision_count

    @property
    def traveler_run_count(self) -> int:
        return self._traveler_run_count

    @property
    def traveler(self):
        return self._traveler

    @property
    def hornets(self):
        return self._hornets

    @staticmethod
    def from_cli_arguments(args: argparse.Namespace) -> "Simulator":
        traveler = Agent(
            Pose(Position(0, args.field_size[1] // 2)),
            Velocity(2, 0),
            Collider(args.traveler_collider_radius),
        )
        hornets = [
            Agent(
                Pose(Position.random_position(args.field_size)),
                Velocity.random_velocity(args.hornet_velocity_range),
                Collider(args.hornet_collider_radius),
            )
            for _ in range(args.hornet_count)
        ]
        return Simulator(traveler, hornets, args.field_size)
