"""
This module contains all classes to define the Rubik's cube
"""
import enum

import numpy as np


class Color(enum.Enum):
    """
    Enumeration containing the six colors of the cube.
    Each color contains the BGR encoding (OpenCV encoding) as its value.
    """

    WHITE = "W"
    ORANGE = "O"
    GREEN = "G"
    RED = "R"
    BLUE = "B"
    YELLOW = "Y"


class Face(enum.Enum):
    """
    Enumeration containing the six positional faces of the cube.
    """

    BACK = enum.auto()
    LEFT = enum.auto()
    TOP = enum.auto()
    RIGHT = enum.auto()
    BOTTOM = enum.auto()
    FRONT = enum.auto()


class Cube:
    """
    Class to define the Rubik's cube and all its operations.
    """

    def __init__(self):
        """
        Constructor of the class, creating a fully solved cube.
        """
        self.faces = {F: np.full((3, 3), C.value) for F, C in zip(Face, Color)}

        self.__solved_state = self.faces.copy()

    def rotate_face(self, face: Face, clockwise: bool = True, double_rot: bool = False):
        """
        Method to rotate a cube's face.

        Parameters
        ----------
        face: Face
            Cube's face to be rotated.
        clockwise: bool, default = True
            If True, the rotation is performed clockwise. If False, the rotation
            is performed counter-clockwise.
        double_rot: bool, default = False
            If True, the rotation is applied as a double rotation. This is equivalent
            to rotating the same face two consecutive times.
        """
        self.faces[face] = np.rot90(
            self.faces[face], axes=(1, 0) if clockwise else (0, 1)
        )

        if face in {Face.TOP, Face.BOTTOM}:
            if (
                face is Face.TOP
                and clockwise is True
                or face is Face.BOTTOM
                and clockwise is False
            ):
                face_order = (Face.FRONT, Face.LEFT, Face.BACK, Face.RIGHT)
            else:
                face_order = (Face.FRONT, Face.RIGHT, Face.BACK, Face.LEFT)
            self.__x_axis_row_rotation(
                row_idx=0 if face is Face.TOP else 1, face_order=face_order
            )

        elif face in {Face.RIGHT, Face.LEFT}:
            if (
                face is Face.RIGHT
                and clockwise is True
                or face is Face.LEFT
                and clockwise is False
            ):
                face_order = (Face.FRONT, Face.TOP, Face.BACK, Face.BOTTOM)
            else:
                face_order = (Face.FRONT, Face.BOTTOM, Face.BACK, Face.TOP)
            self.__y_axis_parallel_rotation(
                front_col_idx=2 if face is Face.RIGHT else 0, face_order=face_order
            )

        else:  # Face is either FRONT or BACK
            if (
                face is Face.FRONT
                and clockwise is True
                or face is Face.BACK
                and clockwise is False
            ):
                pass  # TODO
            self.__y_axis_perpendicular_rotation(
                right_col_idx=0 if face is Face.FRONT else 2, face_order=None
            )

        if double_rot:
            self.rotate_face(face=face, clockwise=clockwise)

    def __x_axis_row_rotation(self, row_idx: int, face_order: tuple):
        """
        Computes and updates the values of the tiles at one single X-axis row from
        the cube. The only two faces that exist purely in this axis are the Top
        and Bottom faces.

        Parameters
        ----------
        row_idx: int
            Index of the row to rotate. This index is the same for all faces to rotate.
        face_order: tuple of Face instances
            Sequence containing the order in which the faces are to be rotated.
        """
        backup_tiles = self.faces[face_order[0]][row_idx]
        self.faces[face_order[0]][row_idx] = self.faces[face_order[1]][row_idx]
        self.faces[face_order[1]][row_idx] = self.faces[face_order[2]][row_idx]
        self.faces[face_order[2]][row_idx] = self.faces[face_order[3]][row_idx]
        self.faces[face_order[3]][row_idx] = backup_tiles

    def __y_axis_parallel_rotation(self, front_col_idx: int, face_order: tuple):
        """
        Computes and updates the values of the tiles at one single Y-axis parallel
        column from the cube. The only two faces that exist purely in this axis are
        the Right and Left faces.

        Parameters
        ----------
        front_col_idx: int
            Column to rotate from the front's face perspective. This index might not
            be the same as the one in the back face, but it is the same as the others.
        face_order: tuple of Face instances
            Sequence containing the order in which the faces are to be rotated.
        """
        if front_col_idx % 2 == 0:
            back_col_idx = 0 if front_col_idx == 2 else 2
        else:
            back_col_idx = 1

        col_idx = tuple(
            back_col_idx if face is Face.BACK else front_col_idx for face in face_order
        )
        backup_tiles = self.faces[face_order[0]][col_idx[0]]
        self.faces[face_order[0]][col_idx[0]] = self.faces[face_order[1]][col_idx[1]]
        self.faces[face_order[1]][col_idx[1]] = self.faces[face_order[2]][col_idx[2]]
        self.faces[face_order[2]][col_idx[2]] = self.faces[face_order[3]][col_idx[3]]
        self.faces[face_order[3]][col_idx[3]] = backup_tiles

    def __y_axis_perpendicular_rotation(self, right_col_idx: int, face_order: tuple):
        """
        Computes and updates the values of the tiles at one single Y-axis perpendicular
        column from the cube. The only two faces that exist purely in this axis are
        the Front and Back faces.

        Parameters
        ----------
        right_col_idx: int
            Column to rotate from the right's face perspective.
        face_order: tuple of Face instances
            Sequence containing the order in which the faces are to be rotated.
        """

    def is_solved(self) -> bool:
        """bool: Whether the cube is solved as in the original state"""
        return self.__solved_state == self.faces
