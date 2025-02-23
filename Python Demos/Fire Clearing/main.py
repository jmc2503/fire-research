#Allow user to show grid environment
from environment import Grid
from algorithm import QLearningAgent, ShortestPathAgent
import matplotlib.pyplot as plt

def main():
    compare_qlearning()


def compare_qlearning(max_size=10, validation_runs=100, max_steps=500):
    
    qlearning_successes_list = []
    qlearning_total_steps_list = []

    shortest_path_successes_list = []
    shortest_path_total_steps_list = []
    
    
    for test in range(2, max_size+1):
        print(f"Testing grid size {test}x{test}")
        env = Grid(0.05, test, test)
        agent = QLearningAgent(env, visualize=False)
        agent.train(episodes=5000)

        state = env.reset(505)
        done = False

        qlearning_successes = 0
        qlearning_total_steps = 0

        #Validate Q-Learning
        for j in range(validation_runs):
            for i in range(max_steps):
                qlearning_total_steps += 1
                action = agent.choose_action(state)
                state, _, done = env.step(action)
                
                if done:
                    qlearning_successes += 1
                    break
            
            env.reset()
        
        #Valid Shortest Path

        agent = ShortestPathAgent(env)
        state = env.reset(505)
        done = False

        shortest_path_successes = 0
        shortest_path_total_steps = 0

        for j in range(validation_runs):
            for i in range(max_steps):
                shortest_path_total_steps += 1
                action = agent.choose_action(state)
                state, _, done = env.step(action)

                if done:
                    shortest_path_successes += 1
                    break
            
            env.reset()
        
        
        qlearning_successes_list.append(qlearning_successes)
        qlearning_total_steps_list.append(qlearning_total_steps)
        shortest_path_successes_list.append(shortest_path_successes)
        shortest_path_total_steps_list.append(shortest_path_total_steps)

        env.close_plot()

    plot_multiple_lists(qlearning_successes_list,shortest_path_successes_list, labels=["Q-Learning Successes", "Shortest Path Successes"], title="Q-Learning vs Shortest Path Successes", xlabel="Grid Size", ylabel="Successes")
    plot_multiple_lists(qlearning_total_steps_list,shortest_path_total_steps_list, labels=["Q-Learning Total Steps", "Shortest Path Total Steps"], title="Q-Learning vs Shortest Path Total Steps", xlabel="Grid Size", ylabel="Total Steps")
        



def plot_multiple_lists(*args, labels=None, title="Plot", xlabel="Index", ylabel="Value"):
    plt.figure()

    for i, arg in enumerate(args):
        if labels and i < len(labels):
            plt.plot(arg, marker='', linestyle='-', label=labels[i])
        else:
            plt.plot(arg, marker='', linestyle='-', label=f"List {i}")
    
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()
        

if __name__ == "__main__":
    main()