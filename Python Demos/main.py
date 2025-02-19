#Allow user to show grid environment
from environment import Grid
from algorithm import QLearningAgent, ShortestPathAgent
import matplotlib.pyplot as plt

max_steps = 50
validation_runs = 100

#To Do List
#Make Q-Learning Better
#    1. 
#Test Shortest Path
#Compare both

def main():
    #Declare the grid and the agent
    env = Grid(0.7, 3, 3)
    
    agent = QLearningAgent(env)

    agent.train(episodes=2000)

    #Display results of training
    state = env.reset(505)
    done = False

    successes = 0
    total_steps = 0

    for j in range(validation_runs):
        for i in range(max_steps):
            total_steps += 1
            action = agent.choose_action(state)
            state, _, done = env.step(action)
            
            if done:
                successes += 1
                break
        
        env.reset()
    
    print(f"Q-Learning Success Rate: {successes}")
    print(f"Q-Learning Total Steps: {total_steps}")

    agent = ShortestPathAgent(env)

    state = env.reset(505)
    successes = 0
    total_steps = 0

    for j in range(validation_runs):
        for i in range(max_steps):
            total_steps += 1
            action = agent.choose_action(state)
            state, _, done = env.step(action)

            if done:
                successes += 1
                break

        env.reset()
    
    print(f"Shortest Path Success Rate: {successes}")
    print(f"Shortest Path Total Steps: {total_steps}")


        

if __name__ == "__main__":
    main()