class Problem:
    def __init__(self, initial, goal=None):
        self.initial = initial
        self.goal = goal

    def actions(self, state):
        raise NotImplementedError

    def result(self, state, action):
        raise NotImplementedError

    def goal_test(self, state):
        if isinstance(self.goal, list):
            # return is_in(state, self.goal)
            return state in self.goal
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        return c + 1

    def value(self, state):
        raise NotImplementedError
    
class RobotNavigation(Problem):
    def __init__(self, grid_parser):
        initial = grid_parser.initial
        goals = grid_parser.goals
        width = grid_parser.grid_w
        height = grid_parser.grid_h
        walls = grid_parser.walls
        super().__init__(initial, goals) # initial and goal are tuples
        # width and height are integers
        self.width = width
        self.height = height
        self.walls = walls # list of tuples

    def actions(self, state):
        """
        Returns the list of possible actions from the current state
        """
        x, y = state
        actions = [
            ('right', (x+1, y)),
            ('down', (x, y+1)),
            ('left', (x-1, y)),
            ('up', (x, y-1)),
        ]

        # Check possible actions
        possible_actions = [action for action in actions if self.check_possible(action[1])]
        return possible_actions

    def result(self, state, action):
        """
        Returns the resulting state after taking the action from the current state
        action format: (action_name, (x, y))
        """
        return action[1]
    
    def check_possible(self, state):
        x, y = state

        # Check if the state is the wall
        for wall_x, wall_y in self.walls:
            if x == wall_x and y == wall_y: return 0

        # Check if the state is out of the grid
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return 0
        
        return 1