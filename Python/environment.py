#Create grid environment NxN with P probability of fire spread
import random

class Grid:
    def __init__(self, p, n):
        self.fire_spread_prob = p #probability of spreading fire
        self.size = n #nxn grid

        self.grid = [["0" for x in range(self.size)] for y in range(self.size)]
        
        self.fire_list = [] #list of all locations with fire
        self.SpreadFire() #Start fire
    
    def SpreadFire(self):
        if self.fire_list.count == 0: #Start fire if not started
            #Generate random location
            x = random.randint(0, self.size-1)
            y = random.randint(0, self.size-1)
            self.fire_list.append((x,y))

            return
        
        new_fires = []

        for fire_loc in self.fire_list:
            if random.random() < self.fire_spread_prob: #spread fire
                new_fires.append(random.choice(self.GetAvailableSpreadLocations(fire_loc))) #create random fire
        
        self.fire_list += new_fires #add new fires



    def GetAvailableSpreadLocations(self, location):
        available = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                if y != x and x + y != 0: #do not allow diagonal fire spread
                    new_location = (location[0] + x, location[1] + y) 
                    if new_location[0] < self.size and new_location >= 0 and new_location[1] < self.size and new_location[1] >= 0:
                        if new_location not in self.fire_list:
                            available.append(new_location)
        
        return available

    def DisplayGrid(self):
        for row in self.grid:
            print(" ".join(row))
        


    

