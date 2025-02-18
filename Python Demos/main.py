#Allow user to show grid environment
from environment import Grid
from algorithm import QLearningAgent
import matplotlib.pyplot as plt

max_steps = 50
validation_runs = 10000

#To Do List
#Make Q-Learning Better
#    1. 
#Test Shortest Path
#Compare both

def main():
    #Declare the grid and the agent
    env = Grid(0.7, 2, 2)
    agent = QLearningAgent(env)

    agent.train(episodes=2000)
    agent.display_reward()

    #Display results of training
    state = env.reset()
    done = False

    successes = 0 

    for j in range(validation_runs):
        for i in range(max_steps):
            action = agent.choose_action(state)
            state, _, done = env.step(action)
            
            if done:
                successes += 1
                break
        
        env.reset()
    
    print(f"Success Rate: {successes}")
    plt.waitforbuttonpress()
        

if __name__ == "__main__":
    main()