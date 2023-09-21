"""
This module contains multiple classes that correspond to the correct notation of the
Rubik's cube
"""
import enum


class NotationEnum(enum.Enum):
    """Extended enumeration with __contains__ applied directly to the values"""
    def __contains__(self, item) -> bool:
        return item in self._value2member_map_


class Color(NotationEnum):
    """
    Enumeration containing the six colors of the cube.
    """

    WHITE = "W"
    ORANGE = "O"
    GREEN = "G"
    RED = "R"
    BLUE = "B"
    YELLOW = "Y"


class CubeFace(NotationEnum):
    """
    Enumeration containing the six positional faces of the cube.
    Each element has the value of its Rubik's cube face notation.
    """

    BACK = "B"
    LEFT = "L"
    TOP = "U"
    RIGHT = "R"
    BOTTOM = "D"
    FRONT = "F"


class CubeSection(NotationEnum):
    """
    Enumeration for the movable sections of the cube, which don't correspond to a face
    """

    MIDDLE_XZ = "M"
    MIDDLE_XY = "E"
    MIDDLE_YZ = "S"


MovesNotation = {
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
}
