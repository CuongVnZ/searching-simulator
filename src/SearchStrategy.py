from collections import deque
from queue import PriorityQueue
from Node import Node

class UninformedSearch:
    """Base class for uninformed search strategies."""

    def __init__(self, problem, renderer=None):
        self.problem = problem
        self.renderer = renderer
        self.created_nodes = 0

    def search(self):
        """Performs the search based on the specific strategy's logic."""
        raise NotImplementedError("Subclasses must implement the search() method.")
    
    def get_name(self):
        """Returns the name of the search strategy."""
        raise NotImplementedError("Subclasses must implement the get_name() method.")
    
    def is_goal(self, node):
        """Checks if the given node is a goal state."""
        return self.problem.goal_test(node.state)
    
    def get_created_nodes(self):
        """Returns the number of created nodes during the search."""

        return self.created_nodes
    
    def visualize(self, explored, frontier):
        """Visualizes the explored and frontier nodes."""

        if self.renderer:
            self.renderer.render(explored, frontier)
        
class InformedSearch(UninformedSearch):
    """Base class for informed search strategies."""

    def manhattan_distance(self, state):
        # Calculate the Manhattan distance to each goal state
        
        # Formula for Manhattan distance: |x1 - x2| + |y1 - y2|
        distances = [abs(state[0] - goal[0]) + abs(state[1] - goal[1]) for goal in self.problem.goal]
        
        # Return the minimum distance among all goal states
        return min(distances)
    

class BreadthFirstSearch(UninformedSearch):
    """Breadth-First Search implementation."""

    def search(self):
        frontier = deque([Node(self.problem.initial)])  # FIFO queue
        explored = set()

        while frontier:
            node = frontier.popleft()
            explored.add(node.state)

            self.created_nodes = len(explored) + len(frontier) + 1
            if self.is_goal(node):
                return node
            
            for child in reversed(node.expand(self.problem)):
                if child.state not in explored and child not in frontier:
                    frontier.append(child)

            self.visualize(explored, frontier)

        return None
    
    def get_name(self):
        return "Breadth-First Search"

class DepthFirstSearch(UninformedSearch):
    """Depth-First Search implementation."""

    def search(self):
        frontier = [Node(self.problem.initial)]  # Stack
        explored = set()

        while frontier:
            node = frontier.pop()
            explored.add(node.state)

            self.created_nodes = len(explored) + len(frontier) + 1
            if self.is_goal(node):
                return node

            for child in node.expand(self.problem):
                if child.state not in explored and child not in frontier:
                # if child.state not in explored:
                    frontier.append(child)

            self.visualize(explored, frontier)

        return None
    
    def get_name(self):
        return "Depth-First Search"

class AStarSearch(InformedSearch):
    """A* Search implementation."""

    def search(self):
        heuristic = self.manhattan_distance
        
        frontier = PriorityQueue()
        frontier.put((0, Node(self.problem.initial)))  # cost, node
        explored = set()
        g_n_list = {self.problem.initial: 0}  # g(n) for each node state

        while not frontier.empty():
            frontier_list = [node[1] for node in list(frontier.queue)]
            _, current_node = frontier.get() # Get the node with the lowest f(n)

            self.created_nodes = len(explored) + len(frontier_list) + 1
            if self.is_goal(current_node):
                return current_node

            explored.add(current_node.state)

            for child in current_node.expand(self.problem):
                if child.state in explored or child in frontier_list:
                    continue

                child_cost = self.problem.path_cost(current_node.path_cost, current_node.state, child.action, child.state)
                g_n = g_n_list[current_node.state] + child_cost
                if child.state not in g_n_list or g_n < g_n_list[child.state]:
                    g_n_list[child.state] = g_n
                    f_n = g_n + heuristic(child.state)
                    frontier.put((f_n, child))

            self.visualize(explored, frontier_list)

        return None
    
    def get_name(self):
        return "A* Search"
    
class GreedyBestFirstSearch(InformedSearch):
    """Greedy Best-First Search implementation."""

    def search(self):
        heuristic = self.manhattan_distance

        frontier = PriorityQueue()
        frontier.put((0, Node(self.problem.initial)))

        explored = set()
        while not frontier.empty():
            frontier_list = [node[1] for node in list(frontier.queue)]
            _, current_node = frontier.get() # Get the node with the lowest f(n)

            self.created_nodes = len(explored) + len(frontier_list) + 1
            if self.is_goal(current_node):
                return current_node

            explored.add(current_node.state)

            for child in current_node.expand(self.problem):
                if child.state not in explored and child not in frontier_list:
                    f_n = heuristic(child.state)
                    frontier.put((f_n, child))
            
            self.visualize(explored, frontier_list)

        return None
    
    def get_name(self):
        return "Greedy Best-First Search"

class CustomSearch1(UninformedSearch):
    """Bidirectional Breadth-First Search."""

    def search(self):
        goals = [goal for goal in self.problem.goal]

        while goals:
            goal = goals.pop() # Process each goal 
            frontier1 = deque([Node(self.problem.initial)])  # Forward frontier
            frontier2 = deque([Node(goal)])  # Backward frontier
            explored1 = set()  # Explored states from forward
            explored2 = set()  # Explored states from backward

            while frontier1 and frontier2:
                # Expand from forward frontier
                node1 = frontier1.popleft()
                explored1.add(node1)

                self.created_nodes = len(explored1) + len(explored2) + len(frontier1) + len(frontier2) + 1
                for child in node1.expand(self.problem):
                    for tmp_node in explored2:
                        if child == tmp_node: # Intersection found
                            return self._construct_path(child, tmp_node.parent)
                    if child not in explored1:
                        frontier1.append(child)

                # Expand from backward frontier
                node2 = frontier2.popleft()
                explored2.add(node2)

                for child in node2.expand(self.problem):
                    # if child in explored1:  # Intersection found
                    #     return self._construct_path(child, explored1)
                    if child not in explored2:
                        frontier2.append(child)

                # Visualization
                frontier = list(frontier1) + list(frontier2)
                explored = []
                for node in explored1:
                    explored.append(node.state)
                for node in explored2:
                    explored.append(node.state)
                self.visualize(explored, frontier)

        return None  # No solution found

    def _construct_path(self, first_half, second_half):
        """Constructs the path from initial state to goal state."""

        path = [first_half]
        while second_half:
            parent = second_half.parent
            previous_node = path[-1]
            second_half.action = self.reverse_action(second_half.state, previous_node.state)
            second_half.parent = previous_node
            path.append(second_half)
            second_half = parent

        return path[-1]

    def reverse_action(self, first, second):
        x1, y1 = first
        x2, y2 = second
        calc = (x1 - x2, y1 - y2)

        actions = [
            ('right', (1, 0)),
            ('down', (0, 1)),
            ('left', (-1, 0)),
            ('up', (0, -1)),
        ]

        for action in actions:
            if action[1] == calc:
                return (action[0], (x1, y1))
            
        return None
    
    def get_name(self):
        return "Bidirectional BFS"

class CustomSearch2(InformedSearch):
    """Beam Search implementation."""

    def search(self):
        heuristic = self.manhattan_distance
        beam_width = 2

        frontier = PriorityQueue()
        frontier.put((0, Node(self.problem.initial)))
        explored = set()

        while not frontier.empty():
            frontier_list = [node[1] for node in list(frontier.queue)]
            _, current_node = frontier.get()

            self.created_nodes = len(explored) + len(frontier_list) + 1
            if self.is_goal(current_node):
                return current_node

            explored.add(current_node.state)

            children = []
            for child in current_node.expand(self.problem):
                if child.state not in explored and child not in frontier_list:
                    children.append(child)

            children.sort(key=lambda x: heuristic(x.state))
            for child in children[:beam_width]:
                frontier.put((heuristic(child.state), child))

            self.visualize(explored, frontier_list)

        return None


    def get_name(self):
        return "CUS2"