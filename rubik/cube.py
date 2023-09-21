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


class CubeFace(enum.Enum):
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


class CubeSection(enum.Enum):
    """
    Enumeration for the movable sections of the cube, which don't correspond to a face
    """

    MIDDLE_XZ = "M"
    MIDDLE_XY = "E"
    MIDDLE_YZ = "S"


class RubiksCube:
    """
    Class to define the Rubik's cube and all its operations.
    """

    def __init__(self):
        """
        Constructor of the class, creating a fully solved cube.
        """
        self.faces = {F: np.full((3, 3), C.value) for F, C in zip(CubeFace, Color)}

        self.__solved_state = self.faces.copy()

    def __str__(self):
        """String representation of the class"""
        return f"""
             {self.faces[CubeFace.TOP][0]}
             {self.faces[CubeFace.TOP][1]}
             {self.faces[CubeFace.TOP][2]}
{self.faces[CubeFace.LEFT][0]}{self.faces[CubeFace.FRONT][0]}{self.faces[CubeFace.RIGHT][0]}{self.faces[CubeFace.BACK][0]}
{self.faces[CubeFace.LEFT][1]}{self.faces[CubeFace.FRONT][1]}{self.faces[CubeFace.RIGHT][1]}{self.faces[CubeFace.BACK][1]}
{self.faces[CubeFace.LEFT][2]}{self.faces[CubeFace.FRONT][2]}{self.faces[CubeFace.RIGHT][2]}{self.faces[CubeFace.BACK][2]}
             {self.faces[CubeFace.BOTTOM][0]}
             {self.faces[CubeFace.BOTTOM][1]}
             {self.faces[CubeFace.BOTTOM][2]}
            """

    def rotate_face(self, face: CubeFace, clockwise: bool, double_rot: bool = False):
        """
        Method to rotate a cube's face.

        Parameters
        ----------
        face: CubeFace
            Cube's face to be rotated.
        clockwise: bool
            If True, the rotation is performed clockwise. If False, the rotation
            is performed counter-clockwise.
        double_rot: bool, default = False
            If True, the rotation is applied as a double rotation. This is equivalent
            to rotating the same face two consecutive times.
        """
        self.faces[face] = np.rot90(
            self.faces[face], axes=(1, 0) if clockwise else (0, 1)
        )

        if face in {CubeFace.TOP, CubeFace.BOTTOM}:
            if (
                face is CubeFace.TOP
                and clockwise is True
                or face is CubeFace.BOTTOM
                and clockwise is False
            ):
                face_order = (
                    CubeFace.FRONT,
                    CubeFace.LEFT,
                    CubeFace.BACK,
                    CubeFace.RIGHT,
                )
            else:
                face_order = (
                    CubeFace.FRONT,
                    CubeFace.RIGHT,
                    CubeFace.BACK,
                    CubeFace.LEFT,
                )
            self.__horizontal_row_rotation(
                row_idx=0 if face is CubeFace.TOP else 2, face_order=face_order
            )

        elif face in {CubeFace.RIGHT, CubeFace.LEFT}:
            if (
                face is CubeFace.RIGHT
                and clockwise is True
                or face is CubeFace.LEFT
                and clockwise is False
            ):
                face_order = (
                    CubeFace.FRONT,
                    CubeFace.TOP,
                    CubeFace.BACK,
                    CubeFace.BOTTOM,
                )
            else:
                face_order = (
                    CubeFace.FRONT,
                    CubeFace.BOTTOM,
                    CubeFace.BACK,
                    CubeFace.TOP,
                )
            self.__vertical_perpendicular_rotation(
                front_col_idx=2 if face is CubeFace.RIGHT else 0, face_order=face_order
            )

        elif face in {CubeFace.FRONT, CubeFace.BACK}:
            if (
                face is CubeFace.FRONT
                and clockwise is True
                or face is CubeFace.BACK
                and clockwise is False
            ):
                face_order = (
                    CubeFace.RIGHT,
                    CubeFace.BOTTOM,
                    CubeFace.LEFT,
                    CubeFace.TOP,
                )
            else:
                face_order = (
                    CubeFace.RIGHT,
                    CubeFace.TOP,
                    CubeFace.LEFT,
                    CubeFace.BOTTOM,
                )
            self.__vertical_parallel_rotation(
                right_col_idx=0 if face is CubeFace.FRONT else 2, face_order=face_order
            )

        if double_rot:
            self.rotate_face(face=face, clockwise=clockwise)

    def rotate_middle_section(
        self, section: CubeSection, frontwards: bool, double_rot: bool = False
    ):
        """
        Method to rotate a middle section of the cube.

        Parameters
        ----------
        section: CubeSection
            Row or column to be rotated. The name of the section should correspond
            to the plane in which the section is contained.
        frontwards: bool
            If True, and depending on the selected section, the rotation is performed
            from Top to Front or from Front to Right. If False, the rotation is the
            inverse as the mentioned ones.
        double_rot: bool, default = False
            If True, the section is rotated twice.
        """
        if section is CubeSection.MIDDLE_XZ:
            if frontwards:
                face_order = (
                    CubeFace.TOP,
                    CubeFace.FRONT,
                    CubeFace.BOTTOM,
                    CubeFace.BACK,
                )
            else:
                face_order = (
                    CubeFace.TOP,
                    CubeFace.BACK,
                    CubeFace.BOTTOM,
                    CubeFace.FRONT,
                )

            self.__vertical_perpendicular_rotation(
                front_col_idx=1, face_order=face_order
            )

        elif section is CubeSection.MIDDLE_XY:
            if frontwards:
                face_order = (
                    CubeFace.FRONT,
                    CubeFace.RIGHT,
                    CubeFace.BACK,
                    CubeFace.LEFT,
                )
            else:
                face_order = (
                    CubeFace.FRONT,
                    CubeFace.LEFT,
                    CubeFace.BACK,
                    CubeFace.RIGHT,
                )

            self.__horizontal_row_rotation(row_idx=1, face_order=face_order)

        if double_rot:
            self.rotate_middle_section(section=section, frontwards=frontwards)

        elif section is CubeSection.MIDDLE_YZ:
            if frontwards:
                face_order = (
                    CubeFace.RIGHT, CubeFace.BOTTOM, CubeFace.LEFT, CubeFace.TOP
                )
            else:
                face_order = (
                    CubeFace.LEFT, CubeFace.BOTTOM, CubeFace.RIGHT, CubeFace.TOP
                )

            self.__vertical_parallel_rotation(right_col_idx=1, face_order=face_order)

    def __horizontal_row_rotation(self, row_idx: int, face_order: tuple):
        """
        Computes and updates the tiles' values of a 1x3x3 cube contained in the
        plane XY.
        Being the rotation around the Z-axis, the only faces that are not updated
        are the Top and Bottom faces.

        Parameters
        ----------
        row_idx: int
            Index of the row to rotate. This index is the same for all faces to rotate.
        face_order: tuple of CubeFace instances
            Sequence containing the order in which the faces are to be rotated.
        """
        backup_tiles = self.faces[face_order[0]][row_idx].copy()
        self.faces[face_order[0]][row_idx] = self.faces[face_order[3]][row_idx]
        self.faces[face_order[3]][row_idx] = self.faces[face_order[2]][row_idx]
        self.faces[face_order[2]][row_idx] = self.faces[face_order[1]][row_idx]
        self.faces[face_order[1]][row_idx] = backup_tiles

    def __vertical_perpendicular_rotation(self, front_col_idx: int, face_order: tuple):
        """
        Computes and updates the tiles' values of a 1x3x3 cube contained in the
        plane XZ.
        Being the rotation around the Y-axis, the only faces that are not updated
        are the Right and Left faces.

        Parameters
        ----------
        front_col_idx: int
            Column to rotate from the front's face perspective. This index might not
            be the same as the one in the back face, but it is the same as the others.
        face_order: tuple of CubeFace instances
            Sequence containing the order in which the faces are to be rotated.
        """
        if front_col_idx % 2 == 0:
            back_col_idx = 0 if front_col_idx == 2 else 2
        else:
            back_col_idx = 1

        col_idx = tuple(
            back_col_idx if face is CubeFace.BACK else front_col_idx
            for face in face_order
        )
        backup_tiles = self.faces[face_order[0]][col_idx[0]].copy()
        self.faces[face_order[0]][:, col_idx[0]] = self.faces[face_order[3]][
            :, col_idx[3]
        ]
        self.faces[face_order[3]][:, col_idx[3]] = self.faces[face_order[2]][
            :, col_idx[2]
        ]
        self.faces[face_order[2]][:, col_idx[2]] = self.faces[face_order[1]][
            :, col_idx[1]
        ]
        self.faces[face_order[1]][:, col_idx[1]] = backup_tiles

    def __vertical_parallel_rotation(self, right_col_idx: int, face_order: tuple):
        """
        Computes and updates the tiles' values of a 1x3x3 cube contained in the
        plane YZ.
        Being the rotation around the X-axis, the only faces that are not updated
        are the Front and Back faces.

        Parameters
        ----------
        right_col_idx: int
            Column to rotate from the right's face perspective.
        face_order: tuple of CubeFace instances
            Sequence containing the order in which the faces are to be rotated.
            The first face should always be the Right face.
        """
        if right_col_idx == 0:
            pos_idx = tuple(
                0 if f in {CubeFace.RIGHT, CubeFace.BOTTOM} else 2 for f in face_order
            )
        elif right_col_idx == 2:
            pos_idx = tuple(
                2 if f in {CubeFace.RIGHT, CubeFace.BOTTOM} else 0 for f in face_order
            )
        else:
            pos_idx = (1, 1, 1, 1)

        backup_tiles = self.faces[face_order[0]][:, pos_idx[0]].copy()
        self.faces[face_order[0]][:, pos_idx[0]] = self.faces[face_order[3]][pos_idx[3]]
        self.faces[face_order[3]][pos_idx[3]] = self.faces[face_order[2]][:, pos_idx[2]]
        self.faces[face_order[2]][:, pos_idx[2]] = self.faces[face_order[1]][pos_idx[1]]
        self.faces[face_order[1]][pos_idx[1]] = backup_tiles

    def is_solved(self) -> bool:
        """bool: Whether the cube is solved as in the original state"""
        return np.all([np.all(face == face[0, 0]) for face in self.faces.values()])
