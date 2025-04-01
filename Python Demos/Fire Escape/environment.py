import random
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
import numpy as np

REWARDS = {
    "escape": 1000,   # Reaching exit
    "fire_penalty": -1000,  # Stepping on fire
    "move_penalty": -0.1,   # Slight penalty for movement
    "distance_reward": 4,   # More reward for moving towards exit
    "do_nothing": -5   # Less punishing for waiting
}

class Grid:
    def __init__(self, m, n, spread_prob=1, num_start_fires=1,visualize=False):
        
        #mxn grid
        self.size_x = m
        self.size_y = n
       
        #Probabilty of fire spreading
        self.fire_spread_probability = spread_prob
        self.num_start_fires = num_start_fires
        
        #List of exit locations
        self.exit_list = []

        self.reset()
        if(visualize):
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
        for i in range(self.num_start_fires):
            x, y = random.randint(0, self.size_x-1), random.randint(0, self.size_y-1)
            self.fire_grid[x][y] = 1
        
        #Reset Agent Pos
        self.agent_pos = (random.randint(0, self.size_x-1), random.randint(0, self.size_y-1))

        #Generate Exits
        self.exit_list = self.generate_exits()

        for ex, ey in self.exit_list:
            self.fire_grid[ex][ey] = 2

        return self.get_next_state()

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
            
        old_agent_pos = self.agent_pos 
        #Move the agent
        new_x, new_y = self.agent_pos[0] + dx, self.agent_pos[1] + dy
        if new_x >= 0 and new_x < self.size_x and new_y >= 0 and new_y < self.size_y:
            self.agent_pos = (new_x, new_y)
            
        reward = self.get_reward(self.agent_pos, old_agent_pos)
        done = 0

        #Check terminal conditions
        if self.fire_grid[self.agent_pos[0]][self.agent_pos[1]] == 1:
            done = 2 #fail
        if self.agent_pos in self.exit_list:
            done = 1 #success
        
        self.spread_fire()
        
        return self.get_next_state(), reward, done

    def get_reward(self, new_agent_pos, old_agent_pos):
        if new_agent_pos in self.exit_list:
            return REWARDS['escape']
        elif self.fire_grid[new_agent_pos[0]][new_agent_pos[1]] == 1:
            return REWARDS['fire_penalty']
        elif new_agent_pos == old_agent_pos:
            return REWARDS['do_nothing']
        
        shortest_distance = float('inf')
        closest_exit = self.exit_list[0]
        for exit in self.exit_list:
            if self.get_distance(old_agent_pos, exit) < shortest_distance:
                closest_exit = exit
                shortest_distance = self.get_distance(old_agent_pos, exit)
        
        if self.get_distance(new_agent_pos, closest_exit) < shortest_distance:
            return REWARDS['distance_reward']

        return REWARDS['move_penalty']
        
    def get_distance(self, start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    def get_next_state(self):
        distances = [self.get_distance(self.agent_pos, exit) for exit in self.exit_list]
        min_distance = min(distances)

        # Nearby fire count (Up, Down, Left, Right)
        x, y = self.agent_pos
        
        fire_neighbors = np.zeros((3, 3), dtype=int)  # 3x3 grid initialized to 0

        for dx in range(-1, 2):  # -1, 0, 1
            for dy in range(-1, 2):  # -1, 0, 1
                nx, ny = x + dx, y + dy  # Neighboring cell coordinates

                # Check if within bounds
                if 0 <= nx < self.size_x and 0 <= ny < self.size_y:
                    fire_neighbors[dx + 1][dy + 1] = self.fire_grid[nx][ny]  # 1 if on fire, 0 if not
            
        # fire_neighbors = sum([
        #     self.fire_grid[x-1][y] if x > 0 else 0,  
        #     self.fire_grid[x+1][y] if x < self.size_x-1 else 0,  
        #     self.fire_grid[x][y-1] if y > 0 else 0,  
        #     self.fire_grid[x][y+1] if y < self.size_y-1 else 0  
        # ])

        return (self.agent_pos, min_distance, tuple(map(tuple, fire_neighbors)))

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
            for i in range(1,len(path) - 1):
                start = path[i]
                end = path[i + 1]
                arrow = FancyArrowPatch((start[1], start[0]), (end[1], end[0]), mutation_scale=15, arrowstyle='->', color='blue')
                self.ax.add_patch(arrow)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
