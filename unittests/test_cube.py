"""Module to test the correct behaviour of the cube"""
import pytest

from rubik import CubeFace, RubiksCube


def test_initialization():
    """Correct initialization of the cube"""
    cube = RubiksCube()
    assert cube.is_solved(), "The cube has not been initialized as a solved cube."

    cube.scramble()
    # And odd number of random moves cannot get as result a solved cube
    assert not cube.is_solved(), "Could not scramble the cube correctly"

    cube = RubiksCube.from_color_code(
        "GGGGGGGGGoooooooooYYYYYYYYYrrrrrrrrrWWWWWWWWWbbbbbbbbb"
    )
    assert cube.is_solved(), "Issue initializing the cube from a string."

    cube = RubiksCube.from_color_code(
        "BGBGGGWRGBOYYRBGYORGYBWGRGWYGOGOBOGOYGYGYGRGWYOROBGRBG"
    )
    assert not cube.is_solved(), "Issue initializing a scrambled cube from a string."


@pytest.mark.parametrize("face", list(CubeFace))
def test_faces_moves(face: CubeFace):
    """Correct rotation of all the main cube faces"""
