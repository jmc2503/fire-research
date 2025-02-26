#Main
from environment import Grid
from algorithm import ShortestPathAgent
import matplotlib.pyplot as plt

max_steps = 500
verification_runs = 100

def main():
    env = Grid(10, 10, 0.1)
    agent = ShortestPathAgent(env)

    for j in range(verification_runs):
        for i in range(max_steps):
            action = agent.choose_action()
            next_state, reward, done = env.step(action)
            if done:
                break

            env.display_grid(agent.min_path)
            plt.pause(0.2)
        
        env.reset()

if __name__ == '__main__':
    main()