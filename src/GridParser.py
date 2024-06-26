class GridParser:
    def __init__(self, filename):
        self.filename = filename
        self.grid_h = None
        self.grid_w = None
        self.initial = None
        self.goals = []
        self.walls = []
        self.parse()

    def parse(self):
        """
        input format:
        [5,11]
        (0,1)
        (7,0) | (10,3)
        (2,0,2,2)
        (8,0,1,2)
        (10,0,1,1)
        (2,3,1,2)
        (3,4,3,1)
        (9,3,1,1)
        (8,4,2,1)
        """
        with open(self.filename, "r") as file:
            self.grid_h, self.grid_w = map(int, file.readline().strip()[1:-1].split(","))
            self.initial = tuple(map(int, file.readline().strip()[1:-1].split(",")))

            for goal in file.readline().strip().split("|"):
                goal_x, goal_y = map(int, goal.strip()[1:-1].split(","))
                self.goals.append((goal_x, goal_y))

            for line in file:
                wall_x, wall_y, wall_w, wall_h = map(int, line.strip()[1:-1].split(","))
                for i in range(wall_y, wall_y + wall_h):
                    for j in range(wall_x, wall_x + wall_w):
                        self.walls.append((j, i))

            # debug
            # print("Initial state:", self.initial)
            # print("Goal state:", self.goals)
            # print("Grid width:", self.grid_w)
            # print("Grid height:", self.grid_h)
            # print("Walls:", self.walls)