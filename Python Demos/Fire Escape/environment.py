import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
import numpy as np

class Grid:
    def __init__(self, m, n, spread_prob=1):
        
        #mxn grid
        self.size_x = m
        self.size_y = n
       
        #Probabilty of fire spreading
        self.fire_spread_probability = spread_prob
        
        #List of exit locations
        self.exit_list = []

        self.reset()
        self.initialize_plot()

    def initialize_plot(self):
        #initialize plot/grid
        self.fig, self.ax = plt.subplots(figsize=(5,5))
        self.ax.set_xlim(-0.5, self.size_y - 0.5)
        self.ax.set_ylim(-0.5, self.size_x - 0.5)
        self.ax.set_xticks(np.arange(-0.5, self.size_y, 1))
        self.ax.set_yticks(np.arange(-0.5, self.size_x, 1))
        self.ax.grid(True)

        #Create agent location (initially at a dummy location [], [])
        self.agent_plot, = self.ax.plot([], [], 'ro', markersize=15)

        #Draw in the initial fires
        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.fire_grid[x][y] == 1:
                    fire_patch = Rectangle((y - 0.5, x - 0.5), 1, 1, color='orange', alpha=0.8)
                    self.ax.add_patch(fire_patch)
        
        #Draw in the exits
        for exit in self.exit_list:
            exit_patch = Rectangle((exit[1] -0.5, exit[0] -0.5), 1, 1, color='green',alpha=0.5)
            self.ax.add_patch(exit_patch)
        
        #Display interactive plot
        plt.ion()
        plt.show()

    def reset(self):
        #Start Fire
        self.fire_grid = [[0 for _ in range(self.size_y)] for x in range(self.size_x)]
        x, y = random.randint(0, self.size_x-1), random.randint(0, self.size_y-1)
        self.fire_grid[x][y] = 1
        
        #Reset Agent Pos
        self.agent_pos = (random.randint(0, self.size_x-1), random.randint(0, self.size_y-1))

        #Generate Exits
        self.exit_list = self.generate_exits()

    def generate_exits(self):
        exits = []

        #Generate 4 exits, each at one edge of the grid
        exits.append((0, random.randint(0, self.size_y-1)))
        exits.append((self.size_x-1, random.randint(0, self.size_y-1)))
        exits.append((random.randint(0, self.size_x-1), 0))
        exits.append((random.randint(0, self.size_x-1), self.size_y-1))

        return exits

    def spread_fire(self):
        #Hold new fires
        new_fire_grid = [[0 for _ in range(self.size_y)] for x in range(self.size_x)]
        
        #Loop through only the old fire grid
        for i in range(self.size_x):
            for j in range(self.size_y):
                if self.fire_grid[i][j] == 1:
                    new_fire_grid[i][j] = 1 #set current cell on fire

                    #Random spread probability
                    if random.random() < self.fire_spread_probability:
                        direction = random.randint(0, 3)
                        dx, dy = 0, 0
                        if direction == 0: #up
                            dy = 1
                        elif direction == 1: #down
                            dy = -1
                        elif direction == 2: #left
                            dx = -1
                        elif direction == 3: #right
                            dx = 1

                        #Check bounds for valid fire
                        if i+dx >= 0 and i+dx < self.size_x and j+dy >= 0 and j+dy < self.size_y:
                            new_fire_grid[i+dx][j+dy] = 1

        self.fire_grid = new_fire_grid

    def step(self, action):
        #0: left, 1: right, 2: down, 3: up
        dx, dy = 0, 0
        if action == 0:
            dx = -1
        elif action == 1:
            dx = 1
        elif action == 2:
            dy = -1
        elif action == 3:
            dy = 1
            
        #Move the agent
        new_x, new_y = self.agent_pos[0] + dx, self.agent_pos[1] + dy
        if new_x >= 0 and new_x < self.size_x and new_y >= 0 and new_y < self.size_y:
            self.agent_pos = (new_x, new_y)
            
        done = False

        #Check terminal conditions
        if self.fire_grid[self.agent_pos[0]][self.agent_pos[1]] == 1:
            done = True
        if self.agent_pos in self.exit_list:
            done = True
        
        self.spread_fire()
            
        return self.agent_pos, 0, done

    def display_grid(self, path=None):
        row, col = self.agent_pos
        self.agent_plot.set_data([col], [row])

        [p.remove() for p in reversed(self.ax.patches)]

        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.fire_grid[x][y] == 1:
                    fire_patch = Rectangle((y-0.5,x-0.5), 1, 1, color='orange', alpha=0.8)
                    self.ax.add_patch(fire_patch)

        for exit in self.exit_list:
            exit_patch = Rectangle((exit[1] - 0.5, exit[0] - 0.5), 1, 1, color='green', alpha=0.5)
            self.ax.add_patch(exit_patch)
        
        if path is not None:
            for i in range(len(path) - 1):
                start = path[i]
                end = path[i + 1]
                arrow = FancyArrowPatch((start[1], start[0]), (end[1], end[0]), mutation_scale=15, arrowstyle='->', color='blue')
                self.ax.add_patch(arrow)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
