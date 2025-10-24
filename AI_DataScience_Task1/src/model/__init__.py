from AI_DataScience_Task1.src.model.SlidingDirection import SlidingDirection
from AI_DataScience_Task1.src.model.State import State
from AI_DataScience_Task1.src.model.TreeNode import TreeNode
import time
import copy
import statistics


def oneRunManhattanHamming(results):
    start = State()
    # print("Startzustand:")
    # print(start)
    # print()

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
    # print("=== Vergleich Hamming vs Manhattan ===")
    # print(f"{'Heuristik':<12} {'Züge':<6} {'Knoten':<10} {'Zeit [s]':<10}")
    # print("-" * 50)
    # print(f"{'Manhattan':<12} "
    #       f"{(len(solution_path_manhattan) - 1) if solution_path_manhattan else '-':<6} "
    #       f"{nodes_manhattan:<10} "
    #       f"{time_manhattan:<10.4f}")
    # print(f"{'Hamming':<12} "
    #       f"{(len(solution_path_hamming) - 1) if solution_path_hamming else '-':<6} "
    #       f"{nodes_hamming:<10} "
    #       f"{time_hamming:<10.4f}")
    # print("-" * 50)
    algo = "manhattan"
    for i in range(2):
        results[algo]["run"] += 1
        results[algo]["solved"] += 1
        if algo == "manhattan":
            results[algo]["times"].append(time_manhattan)
            results[algo]["nodes"].append(nodes_manhattan)
            results[algo]["path_lengths"].append(len(solution_path_manhattan))
        else:
            results[algo]["times"].append(time_hamming)
            results[algo]["nodes"].append(nodes_hamming)
            results[algo]["path_lengths"].append(len(solution_path_hamming))
        algo = "hamming"


def oneRunManhattan(results):
    """
    Führt eine A*-Suche mit der Manhattan-Heuristik aus
    und speichert die Ergebnisse im results-Dictionary.
    """
    start = State()
    node_manhattan = TreeNode(copy.deepcopy(start))

    # === Laufzeit messen ===
    t0 = time.perf_counter()
    solution_path_manhattan, nodes_manhattan = node_manhattan.solve_by_heuristic(lambda s: s.manhattan_cost())
    t1 = time.perf_counter()
    time_manhattan = t1 - t0

    # === Ergebnisse speichern ===
    results["manhattan"]["run"] += 1
    if solution_path_manhattan is not None:
        results["manhattan"]["solved"] += 1
        results["manhattan"]["times"].append(time_manhattan)
        results["manhattan"]["nodes"].append(nodes_manhattan)
        results["manhattan"]["path_lengths"].append(len(solution_path_manhattan) - 1)
    else:
        print("Keine Lösung gefunden (State evtl. unlösbar).")


if __name__ == "__main__":
    results = {
        "hamming": {"run": 0, "times": [], "nodes": [], "solved": 0, "path_lengths": []},
        "manhattan": {"run": 0, "times": [], "nodes": [], "solved": 0, "path_lengths": []},
    }
    for i in range(100):
        oneRunManhattanHamming(results)

    print("\n=== Results Summary ===")
    for heuristic, data in results.items():
        print(f"\n{heuristic.capitalize()}:")
        print(f"  Runs:                 {data['run']}")
        print(f"  Solved:               {data['solved']}")
        print(f"  Total Times:          {sum(data['times'])} seconds")
        print(f"  Nodes:                {sum(data['nodes'])}")
        print(f"  Path Lengths total:   {sum(data['path_lengths'])}")
