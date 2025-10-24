import copy
import random

from AI_DataScience_Task1.src.model.SlidingDirection import SlidingDirection


class State:
    def __init__(self, size=3, board=None):
        self.size = size
        if board:
            self.board = board
        else:
            self.board = None
            self.randomize()

    def __eq__(self, other):
        return isinstance(other, State) and self.get_flat() == other.get_flat()

    def __hash__(self):
        return hash(tuple(self.get_flat()))

    def __str__(self):
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
        return [n for row in self.board for n in row]

    def randomize(self):
        while self.board is None or not self.is_solvable():
            nums = list(range(1, self.size * self.size)) + [None]
            random.shuffle(nums)
            self.board = [nums[i:i + self.size] for i in range(0, len(nums), self.size)]

    def find_empty(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.board[y][x] is None:
                    return x, y

    def make_move(self, direction: SlidingDirection):
        x, y = self.find_empty()
        dx, dy = direction.delta
        nx, ny = x + dx, y + dy

        if 0 <= nx < self.size and 0 <= ny < self.size:
            new_board = copy.deepcopy(self.board)
            #switching
            new_board[y][x], new_board[ny][nx] = new_board[ny][nx], new_board[y][x]
            return State(self.size, new_board)
        return None

    def is_solvable(self):
        flat = [n for row in self.board for n in row if n is not None]
        inversions = sum(
            1 for i in range(len(flat)) for j in range(i + 1, len(flat)) if flat[i] > flat[j]
        )
        if self.size % 2 == 1:
            return inversions % 2 == 0
        else:
            _, empty_y = self.find_empty()
            return (inversions + empty_y) % 2 == 0

    def is_finished(self):
        correct = list(range(1, self.size * self.size)) + [None]
        return self.get_flat() == correct

    def hamming_cost(self):
        dist = 0
        size = self.size
        goal = list(range(1, size * size)) + [None]
        flat = self.get_flat()

        for i in range(len(flat)):
            value = flat[i]
            if value is None:
                continue
            if value != goal[i]:
                dist += 1
        return dist

    def manhattan_cost(self):#
        dist = 0
        size = self.size
        flat = self.get_flat()

        for i in range(len(flat)):
            value = flat[i]
            if value is None:
                continue

            current_row = i // size
            current_col = i % size

            goal_row = (value - 1) // size
            goal_col = (value - 1) % size

            dist += abs(current_row - goal_row) + abs(current_col - goal_col)

        return dist