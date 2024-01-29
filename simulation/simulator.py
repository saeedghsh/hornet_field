"""Entry point for the Hornet Field"""

import argparse
import copy
from typing import List, Sequence

from simulation.agents import Agent, Collider, Pose, Position, Velocity


class Simulator:
    # pylint: disable=missing-class-docstring
    # pylint: disable=missing-function-docstring
    def __init__(self, traveler: Agent, hornets: List[Agent], field_size: Sequence[int]):
        self._traveler = traveler
        self._hornets = hornets
        self._field_size = field_size
        self._traveler_run_count = 0

    def tick(self):
        former_velocity = copy.copy(self._traveler.velocity)
        self._traveler.update(self._field_size)
        bounced = former_velocity != self._traveler.velocity
        if bounced:
            self._traveler_run_count += 1
        for hornet in self._hornets:
            hornet.update(self._field_size)

    def collision(self) -> bool:
        for other in self._hornets:
            if self._traveler.does_collide(other):
                return True
        return False

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
            for i in range(args.hornet_count)
        ]
        return Simulator(traveler, hornets, args.field_size)
