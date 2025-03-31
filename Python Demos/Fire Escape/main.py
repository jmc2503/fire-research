#Main
from environment import Grid
from algorithm import ShortestPathAgent, QLearningAgent
import matplotlib.pyplot as plt

max_steps = 500
verification_runs = 1000

def main():
    qlearning_test()

def qlearning_test():
    env = Grid(20, 20, 0.25, 1,visualize=False)
    agent = QLearningAgent(env)

    agent.train(100000)
    agent.epsilon = 0
    successes= 0 

    state = env.reset()

    for test in range(verification_runs):
        for i in range(max_steps):
            action = agent.choose_action(state)
            state, _, done = env.step(action)
            if done != 0:
                if done == 1:
                    print("Success!")
                    successes += 1
                else:
                    print("fire")
                break
        
        state = env.reset()

    
    print("Success Rate: " + str(successes / verification_runs))

def display_test():
    env = Grid(10, 10, 0, 0,visualize=True)
    agent = ShortestPathAgent(env)

    for i in range(max_steps):
        action = agent.choose_action()
        state, reward, done = env.step(action)
        if done != 0:
            break

        env.display_grid(agent.min_path)
        plt.pause(1)

    env.reset()

def success_test():
    total_success_list = []
    success_list = []

    for num_start_fires in range(1, 6):

        for prob in range(0,11):
            print("Testing (prob, fires): (" + str(prob/10) + "," + str(num_start_fires) + ")")        
            env = Grid(20, 20, prob/10,num_start_fires)
            agent = ShortestPathAgent(env)

            state = env.reset()

            successes = 0

            for j in range(verification_runs):

                for i in range(max_steps):
                    action = agent.choose_action(state)
                    state, reward, done = env.step(action)
                    if done != 0:
                        if done == 1: #success
                            successes += 1
                        break

                    #env.display_grid(agent.min_path)
                    #plt.pause(0.2)
            
                state = env.reset()
            success_list.append(successes / verification_runs)

        print(success_list)
        total_success_list.append(success_list.copy())
        success_list.clear()
    
    display_success_rate(total_success_list)

def display_success_rate(success_list):
    plt.figure()  # Set figure size

    print(success_list)
    x = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]

    # Plot each list with a different color & marker
    for list in success_list:
        plt.plot(x, list, marker='o', label=f"List {success_list.index(list) + 1}")

    # Add labels, title, and legend
    plt.xlabel("Fire Spread Rate (%)")
    plt.ylabel("Success Percentage (%)")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.title("Success Rate vs. Fire Spread Rate for Different Number of Starting Fires")
    plt.legend()
    plt.grid(True)  # Add grid for better readability
    plt.show()

if __name__ == '__main__':
    main()