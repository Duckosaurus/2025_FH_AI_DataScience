"""
Module: tree_node.py

Purpose:
Defines the `TreeNode` class, which represents a node within the search tree
used by the A* algorithm.

A `TreeNode` stores:
- A reference to its associated `State` (8-puzzle configuration)
- A reference to its parent node (for path reconstruction)
- The path cost from the start state (g_cost)

The module also implements the core A* search logic. The method
`solve_by_heuristic(...)` performs the A* search and returns the
solution and number of expanded nodes, using a heuristic function
supplied as a parameter.

This class enables the A* solver to efficiently evaluate and traverse
different puzzle configurations to find an optimal solution.
"""

import copy
import heapq  # Used for the priority queue (open_list)
import itertools  # Used to create a unique tie-breaker for the priority queue

from AI_DataScience_Task1.src.model.board_state import State
from AI_DataScience_Task1.src.model.sliding_direction import SlidingDirection


class TreeNode:
    """
    A node in the A* search tree. It wraps a 'State' object to
    store its parent and its 'g_cost' (path cost from start).
    """

    def __init__(self, state=None, parent=None, g_cost=0):
        """
        Initializes a new tree node.

        Inputs:
            state (State, optional): The 8-puzzle board state for this
                                     node. If None, a new random
                                     State is created.
            parent (TreeNode, optional): The node that generated this
                                         node. Used to reconstruct
                                         the path.
            g_cost (int, optional): The cost to get from the start
                                    node to this node (number of moves).
        Outputs:
            None
        """
        if state is None:
            state = State()
        self.state = state
        self.parent = parent
        self.g_cost = g_cost  # g_cost: cost from start to current node

    def solve_by_heuristic(self, heuristic_fn):
        """
        Performs an A* (A-star) search to find the optimal solution
        path from this node's state to the goal state.

        Inputs:
            heuristic_fn (function): A function (like `State.manhattan_cost`
                                     or `State.hamming_cost`) that takes
                                     a `State` object as input and returns
                                     an integer heuristic value (h_cost).

        Outputs:
            tuple (list[State], int):
                - The first element is a list of `State` objects
                  representing the optimal path from start to goal.
                  It is `None` if no solution is found.
                - The second element is an integer representing the
                  total number of nodes *expanded* (visited)
                  during the search.
        """

        start_node = self
        open_list = []  # The priority queue

        # A unique counter to act as a tie-breaker in the priority queue.
        # If two nodes have the same f_cost, the one added first wins.
        # This prevents errors when the heap tries to compare two
        # non-comparable TreeNode objects.
        counter = itertools.count()
        expanded_nodes = 0

        # f_cost = g_cost + h_cost
        # For the start node, g_cost is 0.
        h_cost = heuristic_fn(start_node.state)
        f_cost = h_cost  # 0 + h_cost

        # The priority queue stores tuples of:
        # (f_cost, tie_breaker, node)
        heapq.heappush(open_list, (f_cost, next(counter), start_node))

        # The closed_set stores *States* we have already expanded.
        # Using a set provides fast average lookup time.
        closed_set = set()

        while open_list:
            # Pop the node with the *lowest* f_cost from the priority queue
            _, _, current_node = heapq.heappop(open_list)
            expanded_nodes += 1

            # --- GOAL CHECK ---
            if current_node.state.is_finished():
                # We found the goal. Reconstruct the path and return it
                # along with the number of expanded nodes.
                return self._reconstruct_path(current_node), expanded_nodes

            # Add the *state* of the current node to the closed set
            # to avoid re-expanding it.
            closed_set.add(current_node.state)

            # --- EXPAND NEIGHBORS ---
            for direction in SlidingDirection:
                # Generate a potential new state
                neighbor_state = current_node.state.make_move(direction)

                # Pruning:
                # 1. If neighbor_state is None, the move was invalid (off-board).
                # 2. If neighbor_state is in closed_set, we have already
                #    processed a better or equal path to this state.
                if not neighbor_state or neighbor_state in closed_set:
                    continue

                # This is a new, valid neighbor. Calculate its costs.
                # g_cost is the cost from start, so it's the parent's
                # g_cost plus 1 (for the single move).
                g_cost = current_node.g_cost + 1
                h_cost = heuristic_fn(neighbor_state)
                f_cost = g_cost + h_cost

                # Create the new neighbor node
                neighbor_node = TreeNode(neighbor_state,
                                         parent=current_node,
                                         g_cost=g_cost)

                # Add the neighbor to the priority queue
                heapq.heappush(open_list,
                               (f_cost, next(counter), neighbor_node))

        # If the open_list becomes empty and we haven't found the goal,
        # then no solution exists.
        return None, expanded_nodes

    def _reconstruct_path(self, node):
        """
        A private helper method to walk backward from the goal node
        to the start node, collecting all states along the way.

        Inputs:
            node (TreeNode): The *goal* node that was found by the
                             search.

        Outputs:
            list[State]: A list of `State` objects representing the
                         path from the *start* to the *goal*, in
                         the correct order.
        """
        path = []
        # Loop backward from the goal node, following the .parent links
        while node:
            path.append(node.state)
            node = node.parent

        # The path was built backward (Goal -> ... -> Start),
        # so reverse it to get (Start -> ... -> Goal).
        path.reverse()
        return path

    def copy_node(self):
        """
        Creates a deep copy of this node, but with no parent.
        (Not used in the main benchmark, but useful for other
         applications).

        Inputs:
            None

        Outputs:
            TreeNode: A new TreeNode with a deep-copied state and
                      no parent.
        """
        return TreeNode(copy.deepcopy(self.state), parent=None)