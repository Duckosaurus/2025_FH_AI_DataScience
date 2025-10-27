"""
Module: run_benchmark.py

Purpose:
This script benchmarks the performance of two A* heuristics for the 8-puzzle:
- Manhattan distance
- Hamming distance

The script runs multiple randomly generated, valid puzzle configurations and solves
each configuration twice: once with each heuristic.

For every solve, it measures:
- Execution time (runtime)
- Number of expanded nodes (search effort)
- Peak memory usage (during solving)
- Solution path length (to verify optimality)

After all runs finish, the script prints a statistical evaluation comparing
both heuristics, including mean and standard deviation values.

This allows a fair and repeatable performance comparison between both
heuristic functions as required for the assignment.
"""


from AI_DataScience_Task1.src.model.board_state import State
from AI_DataScience_Task1.src.model.tree_node import TreeNode
import time
import copy
import statistics
import tracemalloc


def oneRunManhattanHamming(results):
    """
    Runs one benchmark test on a newly generated 8-puzzle instance.

    The puzzle is solved twice:
    1) using the Manhattan heuristic
    2) using the Hamming heuristic

    For each heuristic, the function measures:
    - execution time
    - memory usage
    - number of expanded nodes
    - path length

    All collected data is stored in the given results dictionary.

    Parameters:
        results (dict): A shared dictionary that stores the performance data.
                        The function updates this dictionary directly.

    Returns:
        None
    """

    # 1. Create a single, random, solvable start state
    start = State()

    # 2. Create deep copies of the start node. This is
    #    to ensure both heuristics are benchmarked on the
    #    exact same puzzle.
    node_hamming = TreeNode(copy.deepcopy(start))
    node_manhattan = TreeNode(copy.deepcopy(start))

    # === Manhattan Heuristic Benchmark ===
    tracemalloc.start()  # Start memory tracking
    t0 = time.perf_counter()  # Start timer

    # Run the A* solver, passing the manhattan_cost method as the
    # heuristic function to use.
    path_manhattan, nodes_manhattan = node_manhattan.solve_by_heuristic(
        lambda s: s.manhattan_cost()
    )

    t1 = time.perf_counter()  # Stop timer
    _, peak = tracemalloc.get_traced_memory()  # Get peak memory
    tracemalloc.stop()  # Stop memory tracking

    time_manhattan = t1 - t0
    memory_manhattan = peak / (1024 * 1024)  # Convert bytes to MB

    # The path includes the start state, so length - 1 = moves
    len_manhattan = 0
    if path_manhattan:
        len_manhattan = len(path_manhattan) - 1


    # === Hamming Heuristic Benchmark ===
    tracemalloc.start()
    t0 = time.perf_counter()

    # Run the A* solver, passing the hamming_cost method.
    path_hamming, nodes_hamming = node_hamming.solve_by_heuristic(
        lambda s: s.hamming_cost()
    )

    t1 = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    time_hamming = t1 - t0
    memory_hamming = peak / (1024 * 1024)  # Convert bytes to MB

    len_hamming = 0
    if path_hamming:
        len_hamming = len(path_hamming) - 1

    # === Store results in the main dictionary ===

    # Store results for Manhattan
    results["manhattan"]["solved"] += 1
    results["manhattan"]["times"].append(time_manhattan)
    results["manhattan"]["nodes"].append(nodes_manhattan)
    results["manhattan"]["memory"].append(memory_manhattan)
    results["manhattan"]["lengths"].append(len_manhattan)

    # Store results for Hamming
    results["hamming"]["solved"] += 1
    results["hamming"]["times"].append(time_hamming)
    results["hamming"]["nodes"].append(nodes_hamming)
    results["hamming"]["memory"].append(memory_hamming)
    results["hamming"]["lengths"].append(len_hamming)


# This block ensures the code only runs when the script is
# executed directly (not when imported as a module).
if __name__ == "__main__":

    # This dictionary will store the lists of all results
    results = {
        "hamming": {"times": [], "nodes": [], "solved": 0, "memory": [], "lengths": []},
        "manhattan": {"times": [], "nodes": [], "solved": 0, "memory": [], "lengths": []},
    }

    # Number of random puzzles to solve
    num_runs = 100
    print(f"Running {num_runs} random states for each heuristic...\n")

    # === Main Benchmark Loop ===
    for i in range(num_runs):
        oneRunManhattanHamming(results)
        # Print a progress update every 10 runs
        if (i + 1) % 10 == 0:
            print(f"  ... {i + 1}/{num_runs} completed.")

    # === Report Generation ===
    print(f"\n{'=' * 70}")
    print(f"BENCHMARK REPORT - {num_runs} Random States")
    print(f"{'=' * 70}\n")

    # This will hold the final calculated stats (mean, stdev)
    comparison_data = {}

    # Loop through the results for each heuristic (hamming, manhattan)
    for heuristic, data in results.items():
        print(f"{heuristic.upper()} HEURISTIC")
        print(f"{'-' * 70}")

        if data['solved'] > 0:
            # --- Calculate Metrics ---
            total_nodes = sum(data['nodes'])
            mean_nodes = statistics.mean(data['nodes'])
            stdev_nodes = statistics.stdev(
                data['nodes']) if data['solved'] > 1 else 0.0

            total_time = sum(data['times'])
            mean_time = statistics.mean(data['times'])
            stdev_time = statistics.stdev(
                data['times']) if data['solved'] > 1 else 0.0

            mean_memory = statistics.mean(data['memory'])
            stdev_memory = statistics.stdev(
                data['memory']) if data['solved'] > 1 else 0.0

            total_length = sum(data['lengths'])

            # Store final stats for the summary report
            comparison_data[heuristic] = {
                'mean_nodes': mean_nodes,
                'stdev_nodes': stdev_nodes,
                'mean_time': mean_time,
                'mean_memory': mean_memory,
                'total_length': total_length
            }

            # --- Display Individual Heuristic Report ---
            print(f"Puzzles Solved:               {data['solved']:,} / {num_runs}")
            print(f"Total Nodes Expanded:         {total_nodes:,} nodes")
            print(f"Total Runtime:                {total_time:,.2f} seconds")
            print()
            print(f"Nodes Expanded (Memory Effort):")
            print(f"  Mean:                       {mean_nodes:,.2f} nodes")
            print(f"  Standard Deviation:         {stdev_nodes:,.2f} nodes")
            print()
            print(f"Memory Usage (Peak):")
            print(f"  Mean:                       {mean_memory:,.2f} MB")
            print(f"  Standard Deviation:         {stdev_memory:,.2f} MB")
            print()
            print(f"Execution Time:")
            print(f"  Mean:                       {mean_time:,.4f} seconds")
            print(f"  Standard Deviation:         {stdev_time:,.4f} seconds")
            print()
            print(f"Total Path Lengths:           {total_length} moves")
        else:
            print("  No runs solved")

        print(f"\n")

    # === Performance Comparison Summary ===
    if len(comparison_data) == 2:
        hamming = comparison_data.get('hamming')
        manhattan = comparison_data.get('manhattan')

        if hamming and manhattan:
            print(f"{'=' * 70}")
            print(f"PERFORMANCE COMPARISON")
            print(f"{'=' * 70}")

            # Calculate performance ratios
            nodes_ratio = hamming['mean_nodes'] / manhattan['mean_nodes']
            time_ratio = hamming['mean_time'] / manhattan['mean_time']
            memory_ratio = hamming['mean_memory'] / manhattan['mean_memory']

            print(f"Node Efficiency:              Manhattan explores {nodes_ratio:.2f}x fewer nodes")
            print(f"Runtime Efficiency:           Manhattan is {time_ratio:.2f}x faster")
            print(f"Memory Efficiency:            Manhattan uses {memory_ratio:.2f}x less memory")
            print()
            print(f"Optimality:")

            # Check if both heuristics found the same total path length
            if hamming['total_length'] == manhattan['total_length']:
                print(f"  Both heuristics achieved optimal solutions")
                print(f"  (Total path length: {manhattan['total_length']} moves)")
            else:
                print(f"  WARNING: Path lengths differ!")
                print(f"  Manhattan: {manhattan['total_length']} moves")
                print(f"  Hamming: {hamming['total_length']} moves")

            print(f"{'=' * 70}\n")