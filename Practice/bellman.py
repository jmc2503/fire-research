import numpy as np
import itertools
from collections import defaultdict
import ipywidgets as widgets
from IPython.display import display
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.widgets import Slider

M,N = 2, 2
grid_size = M * N

fire_states = list(itertools.product([0,1], repeat=grid_size))
states = [(x, y) for x in range(grid_size) for y in fire_states]

actions = ["left", "right", "up", "down", "do_nothing", "clear_fire"]
action_indices = {a: i for i, a in enumerate(actions)}

# Rewards
rewards = {
    "clear_fire": 5,
    "end_state": 10,   
    "other": -5        
}

# Initialize Q(s,a) values
Q = {state: np.zeros(len(actions)) for state in states}

# Set Q(s,a) = 0 for terminal states
terminal_states = [state for state in states if np.array(state[1]).sum() == 0]

for state in terminal_states:
    Q[state] = np.zeros(len(actions))

gamma = 0.9
threshold = 1e-6

#Two functions to convert representations of the player's position
def rc_to_index(row, col):
    return N * row + col

def index_to_rc(index):
    return index // N , index % N


def fire_spread_outcomes(fire_state):
    grid = np.array(fire_state).reshape(M, N) # Ensure the grid is a NumPy array
    rows, cols = grid.shape

    # Find all 1's in the grid
    ones_positions = [(r, c) for r in range(rows) for c in range(cols) if grid[r, c] == 1]

    # Define possible spread directions
    directions = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}

    # Mapping each "1" to its possible spread locations
    spread_options = {pos: [] for pos in ones_positions}

    for r, c in ones_positions:
        for dr, dc in directions.values():
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:  # Valid empty cell
                spread_options[(r, c)].append((nr, nc))

    # Generate all possible spread combinations
    spread_events = []
    for pos, targets in spread_options.items():
        spread_events.append(targets + [None])  # "None" means no spread

    all_spread_combinations = list(itertools.product(*spread_events))

    # Dictionary to store next states and their probabilities
    next_states = defaultdict(float)

    for spread_combination in all_spread_combinations:
        new_grid = grid.copy()

        # Track how many 1s spread into each cell
        spread_counts = defaultdict(int)

        # Apply spreading
        for spread_target in spread_combination:
            if spread_target:
                spread_counts[spread_target] += 1  # Track how many 1s spread into this cell

        # Create new grid state
        for (r, c), count in spread_counts.items():
            if count > 0:
                new_grid[r, c] = 1  # Set cell to 1 if at least one spread happens

        # Convert grid to a tuple (for dictionary keys) and flatten for state structure
        grid_tuple = tuple(new_grid.flatten())

        # Compute probability of this spread combination
        probability = 1
        for i, spread_target in enumerate(spread_combination):
            if spread_target:
                probability *= 1/4  # Fire had 1/4 chance to spread in that direction
            else:
                probability *= 1/2  # Fire had 1/2 chance to not spread (spreading out of bounds)

        # Sum probabilities for duplicate grids
        next_states[grid_tuple] += probability

    return dict(next_states)

#Return all possible states with their respective rewards and probability
#Format of each item of next_states: (state, probability, reward)
def transition(state, action):
    if state in terminal_states:
        return [(state, 1.0, 0)]  # No future reward

    pos, fire_state = state
    fire_state = np.array(fire_state)
    next_states = []

    row, col = index_to_rc(pos)

    new_row, new_col = row, col

    if action == "left" and col > 0:
        new_col -= 1
    elif action == "right" and col < N - 1:
        new_col += 1
    elif action == "up" and row > 0:
        new_row -= 1
    elif action == "down" and row < M - 1:
        new_row += 1

    new_pos = rc_to_index(new_row, new_col)

    next_states = []
    
    # Clear fire action
    if action == "clear_fire" and fire_state[new_pos] == 1:
        new_fire_state = fire_state.copy()
        new_fire_state[new_pos] = 0  # Clear fire
        
        reward = rewards["clear_fire"]

        # Check if it's now a terminal state
        if np.sum(new_fire_state) == 0:
            return [((new_pos, tuple(new_fire_state)), 1.0, rewards["end_state"])]

        next_states.append(((new_pos, tuple(new_fire_state)), 1.0, reward))
    
    else:  # Any other action
        reward = rewards["other"]

        # Compute all possible fire spread outcomes
        fire_spreads = fire_spread_outcomes(fire_state)

        for spread_fire_state, prob in fire_spreads.items():
            next_states.append(((new_pos, tuple(spread_fire_state)), prob, reward))

    return next_states


def plot_optimal_policy(ax, state_index):
    state = states[state_index]
    pos, fire_state = state
    fire_grid = np.array(fire_state).reshape(M, N)

    ax.clear()
    ax.set_xlim(-0.5, N-0.5)
    ax.set_ylim(-0.5, M-0.5)
    ax.set_xticks(np.arange(-0.5, N, 1))
    ax.set_yticks(np.arange(-0.5, M, 1))
    ax.grid(True)

    # Define arrow properties
    arrow_props = dict(facecolor='black', shrink=0.05)

    # Define action to arrow direction mapping
    action_to_arrow = {
        "left": (-0.3, 0),
        "right": (0.3, 0),
        "up": (0, 0.3),
        "down": (0, -0.3),
        "do_nothing": (0, 0),
        "clear_fire": (0, 0)
    }

    row, col = index_to_rc(pos)
    if state in terminal_states:
        ax.text(col, M-row-1, 'Terminal', ha='center', va='center', color='red')
    else:
        best_action_index = np.argmax(Q[state])
        best_action = actions[best_action_index]
        dx, dy = action_to_arrow[best_action]
        ax.arrow(col, M-row-1, dx, dy, head_width=0.2, head_length=0.2, fc='blue', ec='blue')

    # Plot the fire grid
    for r in range(M):
        for c in range(N):
            if fire_grid[r, c] == 1:
                ax.add_patch(plt.Rectangle((c-0.5, M-r-1.5), 1, 1, fill=True, color='red', alpha=0.5))

    plt.gca().invert_yaxis()
    plt.show()


# Compute Q(s,a) using value iteration
for i in range(1000):  #max steps
    delta = 0 #keep track of change of values
    new_Q = {state: np.zeros(len(actions)) for state in states}
        
    #For each state-action pair, calculate the expected value of taking that action
    for state in states:
        if state in terminal_states:
            continue  # Skip terminal states
            
        for action_idx, action in enumerate(actions):
            next_states = transition(state, action) #gather all possible next states for this state, action pair
            Q_value = 0

            for next_state, prob, reward in next_states:
                max_next_Q = np.max(Q[next_state])
                Q_value += prob * (reward + gamma * max_next_Q) #expected value summation
                
            new_Q[state][action_idx] = Q_value
            delta = max(delta, abs(Q[state][action_idx] - Q_value))


    Q = new_Q  

    if delta < threshold:
        print(f"Converged at {i}")
        break


#DISPLAY OPTIMAL POLICY
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.1, bottom=0.25)

# Create a slider axis
ax_slider = plt.axes([0.1, 0.1, 0.8, 0.03], facecolor='lightgoldenrodyellow')

# Create the slider
state_slider = Slider(ax_slider, 'State Index', 0, len(states)-1, valinit=0, valstep=1)

# Function to update the plot based on the slider value
def update(val):
    state_index = int(state_slider.val)
    ax.clear()
    plot_optimal_policy(ax, state_index)

# Set the update function for the slider
state_slider.on_changed(update)

# Initial plot
plot_optimal_policy(ax, 0)

# Display the plot
plt.show()

# PRINT ACTUAL STATE VALUES

# # Print final Q(s,a) values
# print("\nComputed Q(s,a) values:")
# for state in states:
#     print(f"State {state}: {Q[state]}")

# #Print best action in each state
# for state in states:
#     if state in terminal_states:
#         print(f"State {(state[0],np.array(state[1]).reshape(M,N))}: Terminal")
#     else:
#         best_action_index = np.argmax(Q[state])  # Index of the max Q-value
#         best_action = actions[best_action_index]  # Corresponding action
#         print(f"State {(state[0],np.array(state[1]).reshape(M,N))}: Best Action -> {best_action}")

# #Test Code for Fire Spreading

# initial_grid = [
#     [1, 0]
# ]

# next_states = fire_spread_outcomes(initial_grid)

# # Print the next states and their probabilities
# for state, prob in next_states.items():
#     print(f"State:\n{np.array(state)}\nProbability: {prob:.3f}\n")


