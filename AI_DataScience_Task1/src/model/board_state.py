"""
Module: board_state.py

Purpose
-------
Implements the `State` class, which represents a unique board configuration
of the 8-puzzle and provides all operations required for search algorithms.

Key Responsibilities:
- Represent an 8-puzzle state and optionally generate a random solvable state.
- Support hashing and equality checks to enable fast lookup in CLOSED sets.
- Generate successor states by sliding tiles in valid directions.
- Check solvability of a puzzle via inversion counting.
- Identify whether the current state matches the goal configuration.
- Provide two admissible heuristic functions used by A*:
  1. Hamming distance   → number of misplaced tiles
  2. Manhattan distance → sum of Manhattan distances of all tiles to their goal positions

The `State` class serves as the foundational data structure for optimal 8-puzzle solving.
"""

import copy
import random

# Import the Enum that defines the four possible move directions
from AI_DataScience_Task1.src.model.sliding_direction import SlidingDirection


class State:
    """
    Represents a single state of the N-puzzle (e.g., 8-puzzle).
    """

    def __init__(self, size=3, board=None):
        """
        Initializes the puzzle state.

        Inputs:
            size (int): The dimension of the board (e.g., 3 for a 3x3 board).
            board (list[list[int]]): A 2D list representing a
                                     pre-defined board. If None, a random,
                                     solvable board will be generated.
        Outputs:
            None
        """
        self.size = size
        if board:
            self.board = board
        else:
            # If no board is provided, create a random one
            self.board = None
            self.randomize()

    def __eq__(self, other):
        """
        Checks if two State objects are equal by comparing their boards.

        Inputs:
            other (any): The object to compare against.

        Outputs:
            bool: True if 'other' is a State and its board is identical
                  to this one, False otherwise.
        """
        return isinstance(other, State) and self.get_flat() == other.get_flat()

    def __hash__(self):
        """
        Generates a hash value for the State, allowing it to be stored
        in a set or as a dictionary key (e.g., in a 'closed set').

        Inputs:
            None

        Outputs:
            int: The hash value, based on a tuple of the flattened board.
        """
        return hash(tuple(self.get_flat()))

    def __str__(self):
        """
        Creates a human-readable string representation of the board.

        Inputs:
            None

        Outputs:
            str: A multi-line string visualizing the board, with the
                 empty space (None) represented as '_'.
        """
        board_str = ""
        for row in range(0, len(self.board)):
            for cell in self.board[row]:
                if cell is None:
                    board_str += "_ "
                    continue
                board_str += str(cell) + " "
            if row != len(self.board) - 1:
                board_str += "\n"

        return board_str

    def get_flat(self):
        """
        Helper method to convert the 2D board (list of lists) into a
        1D list.

        Inputs:
            None

        Outputs:
            list: A 1D list of the board's values, read row by row.
        """
        return [n for row in self.board for n in row]

    def randomize(self):
        """
        Generates a random board and ensures it is solvable.
        It will keep generating new random boards until one
        passes the is_solvable() check.

        Inputs:
            None

        Outputs:
            None (it modifies self.board in-place).
        """
        # Create a list of all numbers (1 to size*size - 1) plus one empty 'None'
        nums = list(range(1, self.size * self.size)) + [None]

        # Loop until a solvable board is generated
        while self.board is None or not self.is_solvable():
            random.shuffle(nums)
            # Convert the 1D list back into a 2D board
            self.board = [nums[i:i + self.size] for i in
                          range(0, len(nums), self.size)]

    def find_empty(self):
        """
        Finds the (x, y) coordinates of the empty (None) tile.

        Inputs:
            None

        Outputs:
            tuple[int, int]: The (x, y) coordinates (column, row) of the
                             empty tile.
        """
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] is None:
                    return x, y

    def make_move(self, direction: SlidingDirection):
        """
        Generates a *new* State object by sliding a tile into the
        empty space from the given direction. This method is non-mutating
        (it does not change the current state).

        Inputs:
            direction (SlidingDirection): The direction of the move
                                          (UP, DOWN, LEFT, RIGHT).

        Outputs:
            State: A *new* State object with the resulting board layout.
            None: If the move is invalid (e.g., trying to move
                  off the board).
        """
        # Find the empty space
        x, y = self.find_empty()

        # Get the (dx, dy) change from the direction enum
        dx, dy = direction.delta
        # Calculate the coordinates (nx, ny) of the tile to swap with
        nx, ny = x + dx, y + dy

        # Check if the tile's coordinates are valid (within the board)
        if 0 <= nx < self.size and 0 <= ny < self.size:
            # Create a deep copy to avoid modifying the original state
            new_board = copy.deepcopy(self.board)
            # Perform the swap
            new_board[y][x], new_board[ny][nx] = new_board[ny][nx], \
                                                 new_board[y][x]
            # Return a new State object with the new board
            return State(self.size, new_board)

        # The move was invalid, so return None
        return None

    def is_solvable(self):
        """
        Checks if the current board state is solvable.
        The formula depends on the number of "inversions" (pairs of
        tiles that are in the wrong order) and the grid size.

        - For odd grids (like 3x3): Solvable if inversions are even.
        - For even grids (like 4x4): Solvable if (inversions + row of
          empty space from bottom) is even.

        Inputs:
            None

        Outputs:
            bool: True if the puzzle is solvable, False otherwise.
        """
        # Get a flat list of all numbers, excluding the empty space
        flat = [n for row in self.board for n in row if n is not None]

        # Count the number of inversions
        inversions = sum(
            1 for i in range(len(flat)) for j in range(i + 1, len(flat)) if
            flat[i] > flat[j]
        )

        if self.size % 2 == 1:
            # Odd grid (3x3, 5x5, ...)
            return inversions % 2 == 0
        else:
            # Even grid (2x2, 4x4, ...)
            _, empty_y = self.find_empty()
            # Find the row of the empty space, counting from the bottom (0-indexed)
            empty_y_from_bottom = (self.size - 1) - empty_y
            return (inversions + empty_y_from_bottom) % 2 == 0

    def is_finished(self):
        """
        Checks if the board is in the goal state.
        The goal state is defined as the empty tile in the top-left
        corner (index 0), followed by tiles 1, 2, 3, ... 8.

        Inputs:
            None

        Outputs:
            bool: True if the board matches the goal state, False otherwise.
        """
        # The correct goal state is [None, 1, 2, 3, 4, 5, 6, 7, 8]
        correct = [None] + list(range(1, self.size * self.size))
        return self.get_flat() == correct

    def hamming_cost(self):
        """
        Calculates the Hamming distance heuristic (h-cost).
        This is the count of how many tiles are *not* in their correct
        final position. The empty tile is not counted.

        Inputs:
            None

        Outputs:
            int: The Hamming distance (h-cost).
        """
        dist = 0
        size = self.size
        # The goal state: [None, 1, 2, 3, 4, 5, 6, 7, 8]
        goal = [None] + list(range(1, size * size))
        flat = self.get_flat()

        for i in range(len(flat)):
            value = flat[i]
            if value is None:
                # Do not count the empty space
                continue
            if value != goal[i]:
                # The tile is not in its correct position
                dist += 1
        return dist

    def manhattan_cost(self):
        """
        Calculates the Manhattan distance heuristic (h-cost).
        This is the sum of the "city block" distances (abs(x1-x2) +
        abs(y1-y2)) for each tile from its current position to
        its goal position. The empty tile is not counted.

        Inputs:
            None

        Outputs:
            int: The Manhattan distance (h-cost).
        """
        dist = 0
        size = self.size
        flat = self.get_flat()

        for i in range(len(flat)):
            value = flat[i]
            if value is None:
                # Do not count the empty space
                continue

            # Current position of the tile
            current_row = i // size
            current_col = i % size

            # Goal position for this 'value'
            # The goal for 'value=1' is index 1.
            # The goal for 'value=8' is index 8.
            goal_index = value
            goal_row = goal_index // size
            goal_col = goal_index % size

            # Calculate the Manhattan distance for this single tile
            dist += abs(current_row - goal_row) + abs(current_col - goal_col)

        return dist