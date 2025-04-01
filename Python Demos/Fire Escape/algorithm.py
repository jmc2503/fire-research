import heapq
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import matplotlib.pyplot as plt

class ShortestPathAgent:
    def __init__(self, env):
        self.env = env

    def heuristic(self, start, goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])
    
    def get_neighbors(self,node):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if 0 <= neighbor[0] < self.env.size_x and 0 <= neighbor[1] < self.env.size_y:
                if self.env.fire_grid[neighbor[0]][neighbor[1]] == 0:
                    neighbors.append(neighbor)
        
        return neighbors
    
    def shortest_path(self, start, goal):

        if self.env.fire_grid[goal[0]][goal[1]] != 0:
            return []
        
        open_list = []
        heapq.heappush(open_list,(0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_list:
            current = heapq.heappop(open_list)[1]

            if current == goal:
                return self.reconstruct_path(came_from, current)
            
            #Check each neighbor to the current node
            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                
                #If the node is new or we found a new path with a lower cost
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))
        return []
    
    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def get_action_from_position(self, start, end):
        if end[0] == start[0] - 1: #left
            return 0
        elif end[0] == start[0] + 1: #right
            return 1
        elif end[1] == start[1] - 1: #down
            return 2
        elif end[1] == start[1] + 1: #up
            return 3
    
    def choose_action(self, state):
        start = self.env.agent_pos
        
        self.min_path = []
        min_path_len = float('inf')

        #Get shortest path
        for exit in self.env.exit_list:
            path = self.shortest_path(start, exit)
            if len(path) < min_path_len and len(path) != 0:
                min_path_len = len(path)
                self.min_path = path
            
        #Find action based on direction of shortest path from current position (start)
        if len(self.min_path) > 1:
            next_step = self.min_path[1]
            return self.get_action_from_position(start, next_step)

class QLearningAgent:
    def __init__(self, env, learning_rate=0.5, discount_factor=0.95, epsilon=0.9998, epsilon_decay=0.9998, visualize=False):
        self.env = env

        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay

        self.q_table = {}

        self.episode_reward_list = []

        self.visualize = visualize
    
    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0) #If entry not found, return default 0.0 value

    #Choose action with epsilon-greedy policy 
    def choose_action(self, state, training=False):
        #Only choose random actions if training
        if training:
            if random.random() < self.epsilon:
                return random.randint(0, 3)
            else:
                return self.get_best_action(state)
        else:
            return self.get_best_action(state)
    
    def get_best_action(self, state):
        q_values = [self.get_q_value(state, action) for action in range(4)]
        best_actions = [a for a, q in enumerate(q_values) if q == max(q_values)]
        return random.choice(best_actions)
    
        #Update the current state, action q-value with the Q-Learning equation based on reward and future Q
    def update_q_value(self, state, action, reward, next_state):
        max_future_q = max([self.get_q_value(next_state, action) for action in range(4)])
        current_q = self.get_q_value(state, action)

        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_future_q - current_q)
        self.q_table[(state, action)] = new_q
    
        #Iterate through the environment episodes number of times  
    def train(self, episodes, max_steps=200):

        step_size = episodes / 10

        for episode in range(episodes):
            state = self.env.reset()
            episode_reward = 0
            step_count = 0

            #Print progress
            if episode % step_size == 0:
                print('.', end=" ")

            for step in range(max_steps): #max_steps stops infinite looping
                #Get action and step through the environment
                action = self.choose_action(state,training=True)
                next_state, reward, done = self.env.step(action)
                
                if step == max_steps - 1:
                    reward = -1000
                
                self.update_q_value(state, action, reward, next_state)
                
                # if self.visualize and episode != 0 and episode % 200 == 0:
                #     self.env.display_grid(episode)
                
                state = next_state

                episode_reward += reward
                step_count += 1
                
                #Has the fire been found?
                if done != 0:
                    break
                
            self.epsilon = max(0.1, self.epsilon*self.epsilon_decay)
            self.episode_reward_list.append(episode_reward)
    
    def display_metrics(self):
        plt.figure()
        plt.plot(self.episode_reward_list)


class PPOAgent:
    pass

        