#Main
from environment import Grid
from algorithm import ShortestPathAgent
import matplotlib.pyplot as plt

max_steps = 500
verification_runs = 1000

def main():
    display_test()


def display_test():
    env = Grid(10, 10, 0, 0,visualize=True)
    agent = ShortestPathAgent(env)

    for i in range(max_steps):
        action = agent.choose_action()
        next_state, reward, done = env.step(action)
        if done != 0:
            break

        env.display_grid(agent.min_path)
        plt.pause(1)

    env.reset()

def success_test():
    success_list = []

    for num_start_fires in range(1, 10):

        for prob in range(0,11):
            print("Testing (prob, fires): (" + str(prob/10) + "," + str(num_start_fires) + ")")        
            env = Grid(20, 20, prob/10,num_start_fires)
            agent = ShortestPathAgent(env)

            successes = 0

            for j in range(verification_runs):
                for i in range(max_steps):
                    action = agent.choose_action()
                    next_state, reward, done = env.step(action)
                    if done != 0:
                        if done == 1: #success
                            successes += 1
                        break

                    #env.display_grid(agent.min_path)
                    #plt.pause(0.2)
            
                env.reset()
            success_list.append(successes / verification_runs)

        print(success_list)
        success_list.clear()


if __name__ == '__main__':
    main()