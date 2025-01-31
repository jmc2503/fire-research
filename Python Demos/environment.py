#Create grid environment NxN with P probability of fire spread
import random
import numpy as np

class Grid:
    def __init__(self, p, n):
        self.fire_spread_prob = p #probability of spreading fire
        self.size = n #nxn grid

        self.fire_list = [] #list of all locations with fire
        self.reset()

    def reset(self):
        self.fire_list.clear()
        self.start_fire()
        self.agent_pos = (0,0)
        return self.agent_pos

    def step(self, action):
        x, y = self.agent_pos
        if action == 0 and x > 0:
            x -= 1
        elif action == 1 and x < self.size - 1:
            x += 1
        elif action == 2 and y > 0:
            y -= 1
        elif action == 3 and y < self.size - 1:
            y += 1
        
        self.agent_pos = (x, y)

        done = False
        reward = 0

        if self.agent_pos in self.fire_list:
            self.fire_list.remove(self.agent_pos)
            reward += 20
            if len(self.fire_list) == 0:
                done = True
        else:
            reward += -1

        #Spread fire
        self.spread_fire()

        #Get next observation
        next_state = self.get_closest_fire()

        return next_state, reward, done
    
    def start_fire(self):
        x = random.randint(0, self.size-1)
        y = random.randint(0, self.size-1)
        self.fire_list.append((x,y))
    
    #Start the fire and then spread it at each time step
    def spread_fire(self):
        
        new_fires = []

        for fire_loc in self.fire_list:
            if random.random() < self.fire_spread_prob: #spread fire
                available = self.get_available_spread_locations(fire_loc)
                if len(available) > 0:
                    new_fires.append(random.choice(available)) #create random fire
        
        self.fire_list += new_fires #add new fires

    #See where the fire can spread within the grid
    def get_available_spread_locations(self, location):
        available = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if y != x and x + y != 0: #do not allow diagonal fire spread
                    new_location = (location[0] + x, location[1] + y) 
                    if new_location[0] < self.size and new_location[0] >= 0 and new_location[1] < self.size and new_location[1] >= 0:
                        if new_location not in self.fire_list:
                            available.append(new_location)
        
        return available
    
    #Return net difference between player and closest fire in tuple form (x, y)
    def get_closest_fire(self):
        min_distance = pow(self.size,2)
        min_tuple = (0, 0)
        for fire_pos in self.fire_list:
            x = self.agent_pos[0] - fire_pos[0]
            y = self.agent_pos[1] - fire_pos[1]

            if abs(x) + abs(y) < min_distance:
                min_tuple = (x, y)
        
        return min_tuple

    #Displays the grid in the console
    #A - Agent
    #F - Fire
    def display_grid(self):
        grid = np.zeros((self.size, self.size), dtype=str)
        grid[:,:] = "0"
        for fire_pos in self.fire_list:
            grid[fire_pos] = "F"
        
        grid[self.agent_pos] = "A"
        for row in grid:
            print(" ".join(row))
        
        print()
        


    

