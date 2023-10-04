"""
This module contains multiple classes that correspond to the correct notation of the
Rubik's cube
"""
import enum


class Color(enum.Enum):
    """
    Enumeration containing the six colors of the cube.
    """

    GREEN = "G"
    ORANGE = "O"
    YELLOW = "Y"
    RED = "R"
    WHITE = "W"
    BLUE = "B"


class CubeFace(enum.Enum):
    """
    Enumeration containing the six positional faces of the cube.
    Each element has the value of its Rubik's cube face notation.
    """

    TOP = "U"
    LEFT = "L"
    FRONT = "F"
    RIGHT = "R"
    BACK = "B"
    BOTTOM = "D"


class CubeSection(enum.Enum):
    """
    Enumeration for the movable sections of the cube, which don't correspond to a face.
    """

    MIDDLE_XZ = "M"
    MIDDLE_XY = "E"
    MIDDLE_YZ = "S"


MovesNotation = [
    "U",
    "U'",
    "U2",
    "D",
    "D'",
    "D2",
    "R",
    "R'",
    "R2",
    "L",
    "L'",
    "L2",
    "F",
    "F'",
    "F2",
    "B",
    "B'",
    "B2",
    "M",
    "M'",
    "M2",
    "E",
    "E'",
    "E2",
    "S",
    "S'",
    "S2",
    None,  # Perform no operation (no move)
]
