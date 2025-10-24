import copy

from AI_DataScience_Task1.src.model import State
from AI_DataScience_Task1.src.model.SlidingDirection import SlidingDirection

class TreeNode:
    def __init__(self, state=None, parent=None):
        if state is None:
            state = State()
        self.state = state
        self.parent = parent
        self.children = None

    def generate_neighbors(self):
        self.children = []
        for direction in SlidingDirection:
            new_state = self.state.make_move(direction)
            if new_state and (self.parent is None or new_state.board != self.parent.state.board):
                child = TreeNode(new_state, parent=self)
                self.children.append(child)

    def print_node(self, parent_id=0):
        print("--" + str(parent_id) + "--")
        print(self.state)
        parent_id += 1
        print("--" + str(parent_id) + "--\n")

        for child in self.children:
            child.print_node(parent_id)

    def solve_by_heuristic(self, heuristic_fn):
        return

    def solve_hamming(self):
        if self.state.is_solvable():
            return self.solve_by_heuristic(lambda s: s.hamming_distance())

    def solve_manhattan(self):
        if self.state.is_solvable():
            return self.solve_by_heuristic(lambda s: s.manhattan_distance())

    def copy_node(self):
        return TreeNode(copy.deepcopy(self.state), parent=None)