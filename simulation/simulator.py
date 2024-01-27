"""Entry point for the Hornet Field"""

import argparse
from typing import List, Sequence

from simulation.agents import Agent, Collider, Pose, Position, Velocity, do_collide


class Simulator:
    # pylint: disable=missing-class-docstring
    # pylint: disable=missing-function-docstring
    def __init__(self, traveler: Agent, hornets: List[Agent], field_size: Sequence[int]):
        self._traveler = traveler
        self._hornets = hornets
        self._field_size = field_size

    def tick(self):
        self._traveler.update(self._field_size)
        for hornet in self._hornets:
            hornet.update(self._field_size)

    def collision(self) -> bool:
        return do_collide(self._traveler, self._hornets)

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
                pose=Pose(Position.random_position(args.field_size)),
                velocity=Velocity.random_velocity(args.hornet_velocity_range),
                collider=Collider(args.hornet_collider_radius),
            )
            for i in range(args.hornet_count)
        ]
        return Simulator(traveler, hornets, args.field_size)
