import tkinter as tk
import time

class Visualizer(tk.Canvas):
    def __init__(self, master, problem, size, speed):
        width = problem.width
        height = problem.height
        self.cell_size = size
        self.delay = speed
        super().__init__(master, width=width * self.cell_size, height=height * self.cell_size, bg="white")
        self.problem = problem
        self.agent = None
        self.cells = {}
        self.draw_grid()
        self.draw_walls()

    def get_cell_dim(self, state):
        x, y = state
        x1 = x * self.cell_size
        y1 = y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        return x1, y1, x2, y2

    def draw_cell(self, state, **args):
        if state not in self.cells:
            x1, y1, x2, y2 = self.get_cell_dim(state)
            cid = self.create_rectangle(x1, y1, x2, y2, args)
            self.cells[state] = cid
        else:
            self.itemconfig(self.cells[state], args)

    def draw_grid(self):
        for i in range(self.problem.height):
            for j in range(self.problem.width):
                self.draw_cell((j, i), outline="black")

    def draw_walls(self):
        for wall in self.problem.walls:
            self.draw_cell(wall, fill="black")

    def draw_agent(self, state):
        if self.agent:
            self.delete(self.agent)
        x1, y1, x2, y2 = self.get_cell_dim(state)
        self.agent = self.create_oval(x1, y1, x2, y2, fill="blue")

    def draw_goal(self):
        for goal in self.problem.goal:
            self.draw_cell(goal, fill="green")

    def draw_initial(self):
        self.draw_cell(self.problem.initial, fill="red")

    def draw_explored(self, state):
        self.draw_cell(state, fill="gray")

    def draw_frontier(self, state):
        self.draw_cell(state, fill="yellow")

    def render(self, explored = [], frontier = [], found_path = None):
        time.sleep(self.delay) # Delay between steps in algorithm
        for state in explored: self.draw_explored(state)
        for node in frontier: self.draw_frontier(node.state)

        self.draw_initial()
        self.draw_agent(self.problem.initial)

        if found_path:
            for action in found_path.solution():
                state = self.problem.result(found_path.state, action)
                self.draw_cell(state, fill="aqua")
                self.draw_agent(state)
                time.sleep(self.delay)
                self.update()
                
        self.draw_goal()
        self.update()