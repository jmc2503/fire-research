import random
import numpy as np
import matplotlib.pyplot as plt
import heapq
#icon

#Q-Learning Agent class defined by an env and other hyperparameters
class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.95, epsilon=0.9, epsilon_decay=0.998, visualize=False):
        #External environment
        self.env = env
        
        #Hyperparamaters
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        
        self.q_table = {}

        #Performance Metrics
        self.episode_reward_list = []
        self.epsiode_steps_list = []
        self.visualize = visualize

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0) #If entry not found, return default 0.0 value

    #Choose action with epsilon-greedy policy 
    def choose_action(self, state, training=False):
        #Only choose random actions if training
        if training:
            if state[1][state[0][0]][state[0][1]] == 1: #If fire is on agent, clear it
                return 4
            elif random.random() < self.epsilon:
                return random.randint(0, 5)
            else:
                return np.argmax([self.get_q_value(state, action) for action in range(6)])
        else:
            return np.argmax([self.get_q_value(state, action) for action in range(6)])
    
    #Update the current state, action q-value with the Q-Learning equation based on reward and future Q
    def update_q_value(self, state, action, reward, next_state):
        max_future_q = max([self.get_q_value(next_state, action) for action in range(6)])
        current_q = self.get_q_value(state, action)

        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_future_q - current_q)
        self.q_table[(state, action)] = new_q

    #Iterate through the environment episodes number of times  
    def train(self, episodes, max_steps=500):
        for episode in range(episodes):
            state = self.env.reset()
            episode_reward = 0
            step_count = 0
            for step in range(max_steps): #max_steps stops infinite looping
                #Get action and step through the environment
                action = self.choose_action(state,training=True)
                next_state, reward, done = self.env.step(action)
                self.update_q_value(state, action, reward, next_state)
                
                if self.visualize and episode != 0 and episode % 200 == 0:
                    self.env.display_grid(episode)
                
                state = next_state

                episode_reward += reward
                step_count += 1
                
                #Has the fire been found?
                if done:
                    break
                
            self.epsilon *= self.epsilon_decay
            self.episode_reward_list.append(episode_reward)
            self.epsiode_steps_list.append(step_count)
    
    def display_reward(self):
        plt.figure()
        plt.cla()
        plt.plot(self.episode_reward_list, marker='', linestyle='-')
        plt.plot(self.epsiode_steps_list, marker='', linestyle='-')

        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.title("Line Graph of a List")

        # Show the graph
        plt.show()

#Agent which follows A* pathfinding algorithm to get closest fire
class ShortestPathAgent:
    def __init__(self, env, visualize=False):
        self.env = env
        self.visualize = visualize
    
    def heuristic(self, start, goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    def get_neighbors(self, node):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if 0 <= neighbor[0] < self.env.size_x and 0 <= neighbor[1] < self.env.size_y:
                neighbors.append(neighbor)
        return neighbors

    #Find path to nearest fire
    def shortest_path(self, start, goal): 
        open_list = []
        heapq.heappush(open_list,(0, start))
        came_from ={}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_list:
            current = heapq.heappop(open_list)[1]

            if current == goal:
                return self.reconstruct_path(came_from, current)
            
            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                
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
    
    def get_action_from_positions(self, start, next_step):
        if next_step[0] == start[0] + 1: #right
            return 1
        elif next_step[0] == start[0] - 1: #left
            return 0
        elif next_step[1] == start[1] + 1: #up
            return 3
        elif next_step[1] == start[1] - 1: #down
            return 2
        else: #do nothing
            return 5

    def choose_action(self, state):
        start = state[0] #agent_pos

        shortest_path = None

        for x in range(self.env.size_x):
            for y in range(self.env.size_y):
                if state[1][x][y] == 1:
                    goal = (x, y)
                    new_path = self.shortest_path(start, goal)
                    if shortest_path is None or len(new_path) < len(shortest_path):
                        shortest_path = new_path

        if self.visualize:
            self.env.display_grid(path=shortest_path)

        if shortest_path and len(shortest_path) > 1: #move in proper direction
            next_step = shortest_path[1]
            return self.get_action_from_positions(start, next_step)
        else:
            return 4 #clear_fire
        