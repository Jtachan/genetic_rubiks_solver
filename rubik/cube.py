"""
This module contains all classes to define the Rubik's cube
"""
from __future__ import annotations

import random
import warnings
from typing import Literal, Sequence

import numpy as np

from rubik.notations import Color, CubeFace, CubeSection


class RubiksCube:
    """
    Class to define the Rubik's cube and all its operations.
    """

    def __init__(self):
        """
        Constructor of the class, creating a fully solved cube.
        """
        self.faces = {F: np.full((3, 3), C.value) for F, C in zip(CubeFace, Color)}

        self._moves_notation = {
            # Face rotation operations
            "U": {"func": self.rotate_face, "args": (CubeFace.TOP, True)},
            "U'": {"func": self.rotate_face, "args": (CubeFace.TOP, False)},
            "U2": {"func": self.rotate_face, "args": (CubeFace.TOP, True, True)},
            "D": {"func": self.rotate_face, "args": (CubeFace.BOTTOM, True)},
            "D'": {"func": self.rotate_face, "args": (CubeFace.BOTTOM, False)},
            "D2": {"func": self.rotate_face, "args": (CubeFace.BOTTOM, True, True)},
            "R": {"func": self.rotate_face, "args": (CubeFace.RIGHT, True)},
            "R'": {"func": self.rotate_face, "args": (CubeFace.RIGHT, False)},
            "R2": {"func": self.rotate_face, "args": (CubeFace.RIGHT, True, True)},
            "L": {"func": self.rotate_face, "args": (CubeFace.LEFT, True)},
            "L'": {"func": self.rotate_face, "args": (CubeFace.LEFT, False)},
            "L2": {"func": self.rotate_face, "args": (CubeFace.LEFT, True, True)},
            "F": {"func": self.rotate_face, "args": (CubeFace.FRONT, True)},
            "F'": {"func": self.rotate_face, "args": (CubeFace.FRONT, False)},
            "F2": {"func": self.rotate_face, "args": (CubeFace.FRONT, True, True)},
            "B": {"func": self.rotate_face, "args": (CubeFace.BACK, True)},
            "B'": {"func": self.rotate_face, "args": (CubeFace.BACK, False)},
            "B2": {"func": self.rotate_face, "args": (CubeFace.BACK, True, True)},
            # Section rotation operations
            "M": {
                "func": self.rotate_middle_section,
                "args": (CubeSection.MIDDLE_XZ, True),
            },
            "M'": {
                "func": self.rotate_middle_section,
                "args": (CubeSection.MIDDLE_XZ, False),
            },
            "M2": {
                "func": self.rotate_middle_section,
                "args": (CubeSection.MIDDLE_XZ, True, True),
            },
            "E": {
                "func": self.rotate_middle_section,
                "args": (CubeSection.MIDDLE_XY, True),
            },
            "E'": {
                "func": self.rotate_middle_section,
                "args": (CubeSection.MIDDLE_XY, False),
            },
            "E2": {
                "func": self.rotate_middle_section,
                "args": (CubeSection.MIDDLE_XY, True, True),
            },
            "S": {
                "func": self.rotate_middle_section,
                "args": (CubeSection.MIDDLE_YZ, True),
            },
            "S'": {
                "func": self.rotate_middle_section,
                "args": (CubeSection.MIDDLE_YZ, False),
            },
            "S2": {
                "func": self.rotate_middle_section,
                "args": (CubeSection.MIDDLE_YZ, True, True),
            },
        }

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

    @classmethod
    def from_color_code(cls, cube_str: str) -> RubiksCube:
        """
        Initializes a cube from a string of 27 color values.

        Parameters
        ----------
        cube_str: str
            Values of the cube given in the next face order: Top, Left, Front, Right,
            Back, Bottom.
            Each value must be the initial letter of its color. For example, 'Y' for
            'Yellow'.
        """
        if len(cube_str) != 54:
            raise ValueError("Invalid string given")

        cube = cls()
        faces = iter(CubeFace)
        face = next(faces)

        for idx, color_val in enumerate(cube_str[:9].upper()):
            if idx >= 9:
                idx %= 9
            coordinate = divmod(idx, 3)
            cube[face][coordinate] = Color(color_val).value
            if idx + 1 % 9 == 0 and face is not CubeFace.BOTTOM:
                face = next(faces)

        return cube

    def scramble(self, nof_moves: int = 25):
        """
        Performs random moves on the cube to scramble it.

        Parameters
        ----------
        nof_moves: int, default = 25
            Number of moves takes in consideration to scramble the cube.
        """
        operations = list(self._moves_notation.keys())
        self.perform_operations(random.choices(operations, k=nof_moves))

    def perform_operations(
        self,
        operations: Sequence[
            Literal[
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
            ]
        ],
    ):
        """
        Performs a single or multiple operations, which correspond to the Rubik's
        cube notation of moves.
        More about the Rubik's cube notation:
        https://ruwix.com/the-rubiks-cube/notation/

        Parameters
        ----------
        operations: Sequence of MovesNotation
            Operations to be performed. The supported operations are:
            U, U', U2, D, D', D2, R, R', R2, L, L', L2, F, F', F2, B, B', B2,
            M, M', M2, E, E', E2, S, S' and S2.
        """
        for operation in operations:
            if operation not in self._moves_notation:
                warnings.warn(f"Skipping unrecognized move {operation}.")
                continue

            move = self._moves_notation[operation]
            move["func"](*move["args"])

    def __getitem__(self, face: CubeFace):
        """Returns the specified face"""
        if not isinstance(face, CubeFace):
            raise ValueError(f"Unsupported instance '{type(face)}'.")
        return self.faces[face]

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
                    CubeFace.RIGHT,
                    CubeFace.BOTTOM,
                    CubeFace.LEFT,
                    CubeFace.TOP,
                )
            else:
                face_order = (
                    CubeFace.LEFT,
                    CubeFace.BOTTOM,
                    CubeFace.RIGHT,
                    CubeFace.TOP,
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

    @property
    def color_code(self) -> str:
        """str:
        The color position of all tiles on the cube. The face order in which they are
        returned is Top, Left, Front, Right, Back, Bottom.
        """
        return "".join("".join(self.faces[f].flatten()) for f in CubeFace)
