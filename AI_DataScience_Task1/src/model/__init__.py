from AI_DataScience_Task1.src.model.SlidingDirection import SlidingDirection
from AI_DataScience_Task1.src.model.State import State
from AI_DataScience_Task1.src.model.TreeNode import TreeNode
import time
import copy

if __name__ == "__main__":
    start = State()
    print("Startzustand:")
    print(start)
    print()

    # gleiche Kopien für beide Heuristiken
    node_hamming = TreeNode(copy.deepcopy(start))
    node_manhattan = TreeNode(copy.deepcopy(start))

    # === Manhattan ===
    t0 = time.perf_counter()
    solution_path_manhattan, nodes_manhattan = node_manhattan.solve_by_heuristic(lambda s: s.manhattan_cost())
    t1 = time.perf_counter()
    time_manhattan = t1 - t0

    # === Hamming ===
    t0 = time.perf_counter()
    solution_path_hamming, nodes_hamming = node_hamming.solve_by_heuristic(lambda s: s.hamming_cost())
    t1 = time.perf_counter()
    time_hamming = t1 - t0

    # === Ergebnisanzeige ===
    print("=== Vergleich Hamming vs Manhattan ===")
    print(f"{'Heuristik':<12} {'Gefunden?':<10} {'Züge':<6} {'Knoten':<10} {'Zeit [s]':<10}")
    print("-" * 50)
    print(f"{'Manhattan':<12} "
          f"{str(solution_path_manhattan is not None):<10} "
          f"{(len(solution_path_manhattan) - 1) if solution_path_manhattan else '-':<6} "
          f"{nodes_manhattan:<10} "
          f"{time_manhattan:<10.4f}")
    print(f"{'Hamming':<12} "
          f"{str(solution_path_hamming is not None):<10} "
          f"{(len(solution_path_hamming) - 1) if solution_path_hamming else '-':<6} "
          f"{nodes_hamming:<10} "
          f"{time_hamming:<10.4f}")
    print("-" * 50)
