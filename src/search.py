import tkinter as tk
from Visualizer import *
from Problem import RobotNavigation
from GridParser import *
from SearchStrategy import BreadthFirstSearch, DepthFirstSearch, AStarSearch, GreedyBestFirstSearch, CustomSearch1, CustomSearch2

def runRobotNavigation(filename, method="bfs", vis = False, size = 30, speed = 0.05):
    # Parse the grid file
    grid_parser = GridParser(filename)

    # Create the problem
    problem = RobotNavigation(grid_parser)

    # Create the visualization window
    root = tk.Tk()
    root.title("Visualization" + " - " + filename + " - " + method)

    # Create the grid visualization
    renderer = None
    if vis: 
        renderer = Visualizer(root, problem, size, speed)
        renderer.pack()

    # Solve the problem
    strategy = None
    if method == "bfs":
        strategy = BreadthFirstSearch(problem, renderer)
    elif method == "dfs":
        strategy = DepthFirstSearch(problem, renderer)
    elif method == "astar":
        strategy = AStarSearch(problem, renderer)
    elif method == "gbfs":
        strategy = GreedyBestFirstSearch(problem, renderer)
    elif method == "cus1":
        strategy = CustomSearch1(problem, renderer)
    elif method == "cus2":
        strategy = CustomSearch2(problem, renderer)

    print(filename, method)
    node = strategy.search()
    
    # Print the solution
    if node:
        path = []
        for n in node.solution():
            path.append(n[0])
        print(path, end="")
        if vis:
            renderer.render(found_path=node)
    else:
        print("No goal is reachable", end="")
    
    print(";",strategy.get_created_nodes())

    # Start the Tkinter event loop
    if vis:
        root.mainloop()


# runRobotNavigation("test1.txt", "dfs", True)
# runRobotNavigation("RobotNav-test.txt", "cus1")
# runRobotNavigation("1.txt", "cus1", True)
# runRobotNavigation("2.txt", "dfs", True)

# m = "cus2"
# for i in range(1, 11):
#     runRobotNavigation(f"{i}.txt", m)

# 2.086
# 2.257
# 2.152
# 1.772
# 3.948
# 1.952

from tkinter import *

def main_menu():
    # Define the methods list
    methods = ["BFS", "DFS", "AStar", "GBFS", "CUS1", "CUS2"]

    # Function to handle start button click (replace with your actual logic)
    def start_clicked():
        filename = entry.get()
        size = int(entry2.get())
        speed = float(entry3.get())
        selected_method = clicked.get()
        # Process filename and selected method
        # print(f"Filename: {filename}, Method: {selected_method}")
        method = selected_method.lower()
        runRobotNavigation(filename, method, True, size, speed)

    # Initialize the main window
    root = Tk()
    root.title("Main Menu")

    # Increase window size (adjust width and height as needed)
    root.geometry("240x170")

    # Create filename label and entry field
    filename_label = Label(root, text="Filename:")
    filename_label.grid(row=0, column=0, padx=5, pady=5)
    entry = Entry(root)
    entry.grid(row=0, column=1, padx=5, pady=5)
    entry.insert(0, "RobotNav-test.txt")
    entry.config(width=25)

    # Create dropdown menu
    clicked = StringVar()
    clicked.set(methods[0])  # Set default selection

    dropdown_label = Label(root, text="Method:")
    dropdown_label.grid(row=1, column=0, padx=5, pady=5)
    dropdown = OptionMenu(root, clicked, *methods)
    dropdown.grid(row=1, column=1, padx=5, pady=5)
    dropdown.config(width=10)

    # Create input field for cell size
    cell_size_label = Label(root, text="Map Size:")   
    cell_size_label.grid(row=2, column=0, padx=5, pady=5)
    entry2 = Entry(root)
    entry2.grid(row=2, column=1, padx=5, pady=5)
    entry2.insert(0, "25")
    entry2.config(width=10)

    # Create input field for cell size
    speed_label = Label(root, text="Speed:")   
    speed_label.grid(row=3, column=0, padx=5, pady=5)
    entry3 = Entry(root)
    entry3.grid(row=3, column=1, padx=5, pady=5)
    entry3.insert(0, "0.01")
    entry3.config(width=10)


    # Create start button
    start_button = Button(root, text="Start", command=start_clicked)
    start_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Run the main loop
    root.mainloop()


import sys
if __name__ == "__main__":
    if len(sys.argv) == 3:
        runRobotNavigation(sys.argv[1], sys.argv[2], vis = False)        
    elif len(sys.argv) == 2 and sys.argv[1] == "gui":
        main_menu()
    else:
        print("Usage: python search.py <filename> <method>")
        print("Or: python search.py gui")
        print("Methods: bfs, dfs, astar, gbfs, cus1, cus2")

    