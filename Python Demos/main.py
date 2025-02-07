#Allow user to show grid environment
from environment import Grid
from algorithm import QLearningAgent
import matplotlib.pyplot as plt

def main():
    #Declare the grid and the agent
    env = Grid(0.1, 2, 2)
    agent = QLearningAgent(env)

    agent.train(episodes=1000)
    #agent.display_reward()

    #Display results of training
    state = env.reset()
    env.display_grid()
    done = False

    while not done:
        action = agent.choose_action(state)
        state, _, done = env.step(action)
        env.display_grid()
        print(_)
        print(env.fire_grid)
        print(env.agent_pos)
        plt.pause(0.5)
    
    plt.ioff()
    plt.show()

if __name__ == "__main__":
    main()