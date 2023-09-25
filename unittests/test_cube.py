"""Module to test the correct behaviour of the cube"""
import pytest

from rubik import CubeFace, CubeSection, RubiksCube


def test_initialization():
    """Correct initialization of the cube"""
    cube = RubiksCube()
    assert cube.is_solved(), "The cube has not been initialized as a solved cube."

    cube = RubiksCube.from_color_code(
        "bbbbbbbbbGGGGGGGGGoooooooooYYYYYYYYYrrrrrrrrrWWWWWWWWW"
    )
    assert cube.is_solved(), "Issue initializing the cube from a string."
    assert cube == RubiksCube(), "Problem comparing solved cubes"
    assert (
        cube == "bbbbbbbbbGGGGGGGGGoooooooooYYYYYYYYYrrrrrrrrrWWWWWWWWW"
    ), "Problem comparing solved cubes"

    cube.scramble()
    # And odd number of random moves cannot get as result a solved cube
    assert not cube.is_solved(), "Could not scramble the cube correctly"

    cube = RubiksCube.from_color_code(
        "BGBGGGWRGBOYYRBGYORGYBWGRGWYGOGOBOGOYGYGYGRGWYOROBGRBG"
    )
    assert not cube.is_solved(), "Issue initializing a scrambled cube from a string."


@pytest.mark.parametrize(
    "face, exp_result",
    (
        (CubeFace.TOP, "GGGGGGGGGYYYOOOOOORRRYYYYYYWWWRRRRRROOOWWWWWWBBBBBBBBB"),
        (CubeFace.LEFT, "WGGWGGWGGOOOOOOOOOGYYGYYGYYRRRRRRRRRWWBWWBWWBYBBYBBYBB"),
        (CubeFace.FRONT, "GGGGGGOOOOOBOOBOOBYYYYYYYYYGRRGRRGRRWWWWWWWWWRRRBBBBBB"),
        (CubeFace.RIGHT, "GGYGGYGGYOOOOOOOOOYYBYYBYYBRRRRRRRRRGWWGWWGWWBBWBBWBBW"),
        (CubeFace.BACK, "RRRGGGGGGGOOGOOGOOYYYYYYYYYRRBRRBRRBWWWWWWWWWBBBBBBOOO"),
        (CubeFace.BOTTOM, "GGGGGGGGGOOOOOOWWWYYYYYYOOORRRRRRYYYWWWWWWRRRBBBBBBBBB"),
    ),
)
def test_faces_moves(face: CubeFace, exp_result: str):
    """Correct rotation of all the main cube faces"""
    cube = RubiksCube()
    cube.rotate_face(face=face, clockwise=True)
    assert cube == exp_result, "Failed clockwise rotation"
    cube.rotate_face(face=face, clockwise=False)
    assert cube.is_solved(), "Failed counter-clockwise rotation"


@pytest.mark.parametrize(
    "section, exp_result",
    (
        (CubeSection("M"), "GWGGWGGWGOOOOOOOOOYGYYGYYGYRRRRRRRRRWBWWBWWBWBYBBYBBYB"),
        (CubeSection("E"), "GGGGGGGGGOOOWWWOOOYYYOOOYYYRRRYYYRRRWWWRRRWWWBBBBBBBBB"),
        (CubeSection("S"), "GGGOOOGGGOBOOBOOBOYYYYYYYYYRGRRGRRGRWWWWWWWWWBBBRRRBBB"),
    ),
)
def test_section_move(section: CubeSection, exp_result: str):
    """Correct rotation of all middle sections"""
    cube = RubiksCube()
    cube.rotate_middle_section(section, frontwards=True)
    assert cube == exp_result, "Failed frontwards rotation"
    cube.rotate_middle_section(section, frontwards=False)
    assert cube.is_solved(), "Failed backwards rotation"
