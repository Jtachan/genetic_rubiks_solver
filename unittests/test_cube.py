"""Module to test the correct behaviour of the cube"""
import pytest
from rubik import RubiksCube, CubeFace
import numpy as np


def test_initialization():
    """Correct initialization of the cube"""
    cube = RubiksCube()
    assert cube.is_solved(), "The cube has not been initialized as a solved cube."
    print(cube)

    cube = RubiksCube.from_color_code(
        "GGGGGGGGGoooooooooYYYYYYYYYrrrrrrrrrWWWWWWWWWbbbbbbbbb")
    assert cube.is_solved(), "Issue initializing the cube from a string."
    print(cube)


@pytest.mark.parametrize("face", [face for face in CubeFace])
def test_faces_moves(face: CubeFace):
    """Correct rotation of all the main cube faces"""
