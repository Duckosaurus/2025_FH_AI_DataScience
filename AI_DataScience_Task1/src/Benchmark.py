# benchmark_main.py
# Run and compare Hamming vs Manhattan solvers, tracking time and memory usage.

import time
import tracemalloc

from AI_DataScience_Task1.src.model import State
from AI_DataScience_Task1.src.model.SlidingDirection import SlidingDirection
from AI_DataScience_Task1.src.model.TreeNode import TreeNode


def _bytes_to_mb(b: int) -> float:
    return b / (1024 * 1024)


def _run_with_metrics(label: str, fn):
    tracemalloc.start()
    t0 = time.perf_counter()
    result = fn()
    t1 = time.perf_counter()
    current_bytes, peak_bytes = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return {
        "label": label,
        "result": result,
        "time_sec": t1 - t0,
        "peak_mb": _bytes_to_mb(peak_bytes),
        "solved": result is not None,
    }


class Benchmark:
    """
    Creates an initial State (either provided or default), runs both solvers,
    and prints a compact comparison table with time and memory usage.
    """

    def __init__(self, initial_state: State | None = None):
        self.initial_state = initial_state or State()

    def run(self):
        root = TreeNode(self.initial_state)

        metrics_hamming = _run_with_metrics(
            "Hamming",
            lambda: root.copy_node().solve_hamming()
        )

        metrics_manhattan = _run_with_metrics(
            "Manhattan",
            lambda: root.copy_node().solve_manhattan()
        )

        self._print_summary([metrics_hamming, metrics_manhattan])

    @staticmethod
    def _print_summary(rows):
        # header
        print("\n=== Heuristic Benchmark (time & peak memory) ===")
        print(f"{'Heuristic':<12} {'Solved':<8} {'PathLen':<8} {'Time [s]':<10} {'Peak Mem [MB]':<14}")
        print("-" * 56)
        # rows
        for m in rows:
            print(
                f"{m['label']:<12} "
                f"{str(m['solved']):<8} "
                f"{m['time_sec']:<10.6f} "
                f"{m['peak_mb']:<14.3f}"
            )
        print("-" * 56)
        print("Note: Peak memory via tracemalloc (Python heap only).")


if __name__ == "__main__":
    # Example usage:
    # - Uses State() default constructor. If your State randomizes, both solvers run on the same start state.
    # - If your State may be unsolvable, the .solve_* methods already check is_solvable().
    bench = Benchmark()
    bench.run()
