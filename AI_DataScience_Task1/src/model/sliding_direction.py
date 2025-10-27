"""
Module: sliding_direction.py

Purpose
-------
Defines the four legal directions of tile movement in the 8-puzzle as a
type-safe enumeration. Each enum member stores the coordinate offset
(dx, dy) used to locate the tile that moves into the empty space.

Coordinate System
-----------------
(x, y)
x → column index, increasing to the right
y → row index, increasing downward
(0, 0) is the top-left position on the board.

The direction name represents where the *tile* moves relative to the empty space.
Example: SlidingDirection.DOWN means the tile above the empty space moves downward.
"""

from enum import Enum


class SlidingDirection(Enum):
    """
    Cardinal directions for valid 8-puzzle moves.

    Each member encodes a displacement (dx, dy) used to identify
    the tile adjacent to the empty space that will be slid.
    """

    # The tile above moves down into the empty space
    DOWN = (0, -1)

    # The tile to the right moves left into the empty space
    LEFT = (1, 0)

    # The tile below moves up into the empty space
    UP = (0, 1)

    # The tile to the left moves right into the empty space
    RIGHT = (-1, 0)

    @property
    def delta(self) -> tuple[int, int]:
        """
        Return the coordinate offset (dx, dy) defining the direction.

        Returns
        -------
        tuple[int, int]
            Direction offset to locate the tile that can slide into
            the empty space.
        """
        return self.value
