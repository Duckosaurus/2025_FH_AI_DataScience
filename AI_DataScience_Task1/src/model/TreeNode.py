import copy
import heapq
import itertools

from AI_DataScience_Task1.src.model import State
from AI_DataScience_Task1.src.model.SlidingDirection import SlidingDirection

class TreeNode:
    def __init__(self, state=None, parent=None, g_cost=0):
        if state is None:
            state = State()
        self.state = state
        self.parent = parent
        self.children = None
        self.g_cost = g_cost

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

        if self.children:
            for child in self.children:
                child.print_node(parent_id)

    def solve_by_heuristic(self, heuristic_fn):
        """
        Führt A*-Suche durch.
        heuristic_fn: Funktion, die einen State nimmt und eine Heuristik (int) zurückgibt.
        Gibt den gefundenen Zielknoten zurück oder None.
        """

        start = self
        open_list = []
        counter = itertools.count()  # eindeutiger Tiebreaker

        heapq.heappush(open_list, (heuristic_fn(start.state),next(counter), start))
        closed_set = set()

        while open_list:
            _, _, current = heapq.heappop(open_list)

            if current.state.is_finished():
                # Pfad rückverfolgen
                return self._reconstruct_path(current)

            closed_set.add(current.state)

            # Nachbarn erzeugen
            for direction in SlidingDirection:
                neighbor_state = current.state.make_move(direction)
                if not neighbor_state or neighbor_state in closed_set:
                    continue

                g_cost = current.g_cost + 1
                f_cost = g_cost + heuristic_fn(neighbor_state)
                neighbor_node = TreeNode(neighbor_state, parent=current, g_cost=g_cost)

                heapq.heappush(open_list, (f_cost, next(counter),neighbor_node))

        return None  # keine Lösung gefunden

    def _reconstruct_path(self, node):
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        path.reverse()
        return path

    def solve_hamming(self):
        if self.state.is_solvable():
            print("State is solvable.")
            return self.solve_by_heuristic(lambda s: s.hamming_cost())
        else:
            print("State not solvable.")
            return None

    def solve_manhattan(self):
        if self.state.is_solvable():
            print("State is solvable.")
            return self.solve_by_heuristic(lambda s: s.manhattan_cost())
        else:
            print("State not solvable.")
            return None

    def copy_node(self):
        return TreeNode(copy.deepcopy(self.state), parent=None)