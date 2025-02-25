#Main
from environment import Grid
from algorithm import ShortestPathAgent

max_steps = 500

def main():
    env = Grid(10, 10, 0.1)
    agent = ShortestPathAgent(env)

    for i in range(max_steps):
        action = agent.choose_action()
        next_state, reward, done = env.step(action)
        if done:
            break

        env.display_grid(agent.min_path)

if __name__ == '__main__':
    main()