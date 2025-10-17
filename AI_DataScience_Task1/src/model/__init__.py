from AI_DataScience_Task1.src.model.SlidingDirection import SlidingDirection
from AI_DataScience_Task1.src.model.State import State
from AI_DataScience_Task1.src.model.TreeNode import TreeNode

if __name__ == "__main__":
    s = TreeNode()
    s.generate_neighbors()
    s.print_node()