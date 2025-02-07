import random
import numpy as np
import matplotlib.pyplot as plt
#icon

#Q-Learning Agent class defined by an env and other hyperparameters
class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.95, epsilon=0.9, epsilon_decay=0.98):
        #External environment
        self.env = env
        
        #Hyperparamaters
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        
        self.q_table = {}
        self.episode_reward_list = []

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0) #If entry not found, return default 0.0 value

    #Choose action with epsilon-greedy policy 
    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.randint(0, 5)
        else:
            return np.argmax([self.get_q_value(state, action) for action in range(6)])
    
    #Update the current state, action q-value with the Q-Learning equation based on reward and future Q
    def update_q_value(self, state, action, reward, next_state):
        max_future_q = max([self.get_q_value(next_state, action) for action in range(6)])
        current_q = self.get_q_value(state, action)

        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_future_q - current_q)
        self.q_table[(state, action)] = new_q

    #Iterate through the environment episodes number of times  
    def train(self, episodes, max_steps=100):
        for episode in range(episodes):
            state = self.env.reset()
            episode_reward = 0
            for step in range(max_steps): #max_steps stops infinite looping
                #Get action and step through the environment
                action = self.choose_action(state)
                next_state, reward, done = self.env.step(action)
                self.update_q_value(state, action, reward, next_state)
                state = next_state

                episode_reward += reward
                
                #Has the fire been found?
                if done:
                    break
                
            self.epsilon *= self.epsilon_decay
            self.episode_reward_list.append(episode_reward)
    
    def display_reward(self):
        plt.plot(self.episode_reward_list, marker='o', linestyle='-')

        plt.xlabel("Index")
        plt.ylabel("Value")
        plt.title("Line Graph of a List")

        # Show the graph
        plt.show()

        