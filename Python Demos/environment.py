#Create grid environment NxN with P probability of fire spread
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

#Change state information
    #State becomes (pos, fire grid)
#change fire spread
    #Make it so the spread prob is 1/4 to any direction, only spreads once

REWARDS = {
    "clear_fire": 10,
    "move_penalty": -20,
    "finish_state": 100
}

class Grid:
    def __init__(self, p, size_x, size_y):
        self.fire_spread_prob = p #probability of spreading fire
        
        self.size_x = size_x #nxn grid
        self.size_y = size_y
        
        #list of all locations with fire
        self.reset()
        self.initialize_plot()

    def initialize_plot(self):
        # Set up the grid
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.ax.set_xlim(-0.5, self.size_y - 0.5)
        self.ax.set_ylim(-0.5, self.size_x - 0.5)
        self.ax.set_xticks(np.arange(-0.5, self.size_y, 1))
        self.ax.set_yticks(np.arange(-0.5, self.size_x, 1))
        self.ax.grid(True)

        self.agent_plot, = self.ax.plot([], [], 'ro', markersize=15)

        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.fire_grid[x][y] == 1:
                    fire_patch = Rectangle((y - 0.5, x - 0.5), 1, 1, color='orange', alpha=0.8)
                    self.ax.add_patch(fire_patch)

        plt.ion()  # Turn on interactive mode
        plt.show()

    def reset(self, seed=None):

        if seed is not None:
            random.seed(seed)

        self.start_fire()

        self.agent_pos = (random.randint(0, self.size_x-1), random.randint(0, self.size_y-1))

        return (self.agent_pos, tuple(tuple(row) for row in self.fire_grid))
    
    def start_fire(self):
        #Clear the fire
        self.fire_grid = [[0 for _ in range(self.size_y)] for x in range(self.size_x)] 
        self.num_fires = 0

        #Start the fire
        x = random.randint(0, self.size_x-1)
        y = random.randint(0, self.size_y-1)
        self.fire_grid[x][y] = 1
        self.num_fires += 1

    #Actions:
    #0 = Left, 1 = Right, 2 = Down, 3 = Up, 4 = Put out fire, 5 = do nothing
    def step(self, action):
        x, y = self.agent_pos

        reward = 0
        done = False

        if action == 0 and x > 0:
            x -= 1
        elif action == 1 and x < self.size_x - 1:
            x += 1
        elif action == 2 and y > 0:
            y -= 1
        elif action == 3 and y < self.size_y - 1:
            y += 1
        
        new_agent_pos = (x, y)
        
        #Get reward based on action and new state
        reward = self.reward_function(action, new_agent_pos)

        #Spread Fire if the episode is not done yet
        if self.num_fires == 0:
            done = True
            reward = REWARDS['finish_state']
        else:
            self.spread_fire()

        #Move agent
        self.agent_pos = new_agent_pos

        #Get next observation
        next_state = (self.agent_pos, tuple(tuple(row) for row in self.fire_grid))

        return next_state, reward, done
    
    #Reward function
    #Put out fire: 10
    #Just move: -1
    #Stand on fire without putting out: -10
    def reward_function(self, action, new_agent_pos):
        if action == 4: #clear fire
            if self.fire_grid[new_agent_pos[0]][new_agent_pos[1]] == 1:
                self.fire_grid[new_agent_pos[0]][new_agent_pos[1]] = 0 #remove fire
                self.num_fires -= 1
                return REWARDS['clear_fire']
                
        return REWARDS['move_penalty'] #move penalty
    
    def translate_agent_pos(self):
        return self.size_y * self.agent_pos[0] + self.agent_pos[1]
    
    #Start the fire and then spread it at each time step
    def spread_fire(self):
        
        new_fires = []

        for x in range(len(self.fire_grid)):
            for y in range(len(self.fire_grid[0])):
                if self.fire_grid[x][y] == 1 and random.random() < self.fire_spread_prob: 
                    direction = random.randint(0, 3) #generate random direction 0 = left, 1 = right, 2 = down, 3 = up
                    new_x = x
                    new_y = y

                    if direction == 0:
                        new_x -= 1
                    elif direction == 1:
                        new_x += 1
                    elif direction == 2:
                        new_y -= 1
                    elif direction == 3:
                        new_y += 1
                    
                    new_location = (new_x, new_y)

                    if self.check_valid_spread(new_location):
                        new_fires.append(new_location)
        
        for fire in new_fires:
            if self.fire_grid[fire[0]][fire[1]] != 1:
                self.fire_grid[fire[0]][fire[1]] = 1 #Set new fire
                self.num_fires += 1 #Add fire counter


        # for fire_loc in self.fire_list:
        #     if random.random() < self.fire_spread_prob: #spread fire
        #         available = self.get_available_spread_locations(fire_loc)
        #         if len(available) > 0:
        #             new_fires.append(random.choice(available)) #create random fire

        #self.fire_list += new_fires #add new fires
    
    def check_valid_spread(self, new_location):
        if new_location[0] >= 0 and new_location[0] <= self.size_x - 1 and new_location[1] >= 0 and new_location[1] <= self.size_y - 1:
            if self.fire_grid[new_location[0]][new_location[1]] != 1:
                return True
        
        return False


    #Displays the grid using matplotlib
    def display_grid(self,episode=None):
        row, col = self.agent_pos
        self.agent_plot.set_data([col], [row])  # Flip y-axis

        [p.remove() for p in reversed(self.ax.patches)]

        for x in range(self.size_x):
            for y in range(self.size_y):
                if self.fire_grid[x][y] == 1:
                    fire_patch = Rectangle((y - 0.5, x - 0.5), 1, 1, color='orange', alpha=0.8)
                    self.ax.add_patch(fire_patch)

        if episode is not None:
            self.ax.set_title(f"Episode {episode}")

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        

    #See where the fire can spread within the grid
    # def get_available_spread_locations(self, location):
    #     available = []
    #     for x in range(-1, 2):
    #         for y in range(-1, 2):
    #             if y != x and x + y != 0: #do not allow diagonal fire spread
    #                 new_location = (location[0] + x, location[1] + y) 
    #                 if new_location[0] < self.size and new_location[0] >= 0 and new_location[1] < self.size and new_location[1] >= 0:
    #                     if new_location not in self.fire_list:
    #                         available.append(new_location)
        
    #     return available

    #Return net difference between player and closest fire in tuple form (x, y)
    # def get_closest_fire(self):
    #     min_distance = pow(self.size,2)
    #     min_tuple = (0, 0)
    #     for fire_pos in self.fire_list:
    #         x = self.agent_pos[0] - fire_pos[0]
    #         y = self.agent_pos[1] - fire_pos[1]

    #         if abs(x) + abs(y) < min_distance:
    #             min_tuple = (x, y)
        
    #     return min_tuple

