"""
This module contains a class to perform the genetic algorithm
"""
import random

from typing import Sequence, Optional

from dataclasses import dataclass

import numpy as np

from rubik.cube import RubiksCube
from rubik.notations import MovesNotation, CubeFace


@dataclass
class Candidate:
    cube: RubiksCube
    # moves: Sequence[MovesNotation]


class GeneticSolver:
    """
    Class to perform a genetic algorithm to find the solution of the cube.
    """

    def __init__(self, cube: Optional[RubiksCube] = None, population_size: int = 500):
        if cube is None:
            cube = RubiksCube()
        if cube.is_solved():
            print("Scrambling cube")
            cube.scramble()
        self._initial_cube = cube

        print(self.fitness(Candidate(cube)))

    def fitness(self, candidate: Candidate) -> int:
        cube = candidate.cube

        if cube.is_solved():
            return 100_000

        # Minimum return value = 12 ** 2 = 144
        # Maximum return value = 53 ** 2 = 2809
        nof_correct_tiles = np.sum(
            [np.unique(cube[face], return_counts=True)[1].max() for face in CubeFace]
        )
        return int(nof_correct_tiles ** 2)

    @staticmethod
    def generate_random_candidate(nof_moves: int = 50) -> Sequence[MovesNotation]:
        return random.choices(MovesNotation, k=nof_moves)


if __name__ == '__main__':
    GeneticSolver()
