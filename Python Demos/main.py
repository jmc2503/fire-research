#Allow user to show grid environment
from environment import Grid
from algorithm import QLearningAgent

def main():
    #Declare the grid and the agent
    env = Grid(0.25, 5)
    agent = QLearningAgent(env)

    agent.train(episodes=500)

    #Display results of training
    state = env.reset()
    env.display_grid()
    done = False

    while not done:
        action = agent.choose_action(state)
        state, _, done = env.step(action)
        env.display_grid()

if __name__ == "__main__":
    main()