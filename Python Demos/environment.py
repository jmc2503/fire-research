#Create grid environment NxN with P probability of fire spread
import random
import numpy as np

class Grid:
    def __init__(self, p, n):
        self.fire_spread_prob = p #probability of spreading fire
        self.size = n #nxn grid

        self.fire_list = [] #list of all locations with fire
        self.spread_fire() #Start fire
        self.reset()

    def reset(self):
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

        #Thing to add: make it so multiple fires 
        if self.agent_pos in self.fire_list:
            return self.agent_pos, 10, True #found fire, make this false for multiple fires
        else:
            return self.agent_pos, -1, False #move penalty
    
    def spread_fire(self):
        if self.fire_list.count == 0: #Start fire if not started
            #Generate random location
            x = random.randint(0, self.size-1)
            y = random.randint(0, self.size-1)
            self.fire_list.append((x,y))

            return
        
        new_fires = []

        for fire_loc in self.fire_list:
            if random.random() < self.fire_spread_prob: #spread fire
                new_fires.append(random.choice(self.get_available_spread_locations(fire_loc))) #create random fire
        
        self.fire_list += new_fires #add new fires

    def get_available_spread_locations(self, location):
        available = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if y != x and x + y != 0: #do not allow diagonal fire spread
                    new_location = (location[0] + x, location[1] + y) 
                    if new_location[0] < self.size and new_location >= 0 and new_location[1] < self.size and new_location[1] >= 0:
                        if new_location not in self.fire_list:
                            available.append(new_location)
        
        return available

    def display_grid(self):
        grid = np.zeros((self.size, self.size), dtype=str)
        grid[:,:] = "0"
        for fire_pos in self.fire_list:
            grid[fire_pos] = "F"
        
        grid[self.agent_pos] = "A"
        for row in grid:
            print(" ".join(row))
        


    

