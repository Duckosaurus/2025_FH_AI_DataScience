from AI_DataScience_Task1.src.model.SlidingDirection import SlidingDirection
from AI_DataScience_Task1.src.model.State import State
from AI_DataScience_Task1.src.model.TreeNode import TreeNode

if __name__ == "__main__":
    start = State()
    print("Startzustand:")
    print(start)

    node = TreeNode(start)
    #solution_path_manhattan = node.solve_manhattan()
    solution_path_hamming = node.solve_hamming()

    #if solution_path_manhattan:
        #print(f"\nLösung Manhattan gefunden in {len(solution_path_manhattan) - 1} Zügen:")
        #for step in solution_path_manhattan:
            #print(step)
            #print()
    if solution_path_hamming:
        print(f"\nLösung Hamming gefunden in {len(solution_path_hamming) - 1} Zügen:")

    else:
        print("Keine Lösung gefunden.")
    #s = TreeNode()
    #s.generate_neighbors()
    #s.print_node()