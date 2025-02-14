import numpy as np
import itertools

# Define states (excluding terminal states in computation)
# states = [
#     (0, (1, 0)), (0, (0, 1)), (0, (1, 1)),
#     (1, (1, 0)), (1, (0, 1)), (1, (1, 1)),
#     (0, (0, 0)), (1, (0, 0))  # Terminal states
# ]

M,N = 2, 2
grid_size = M * N
fire_spread_prob = 0.25

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
print(terminal_states)
for state in terminal_states:
    Q[state] = np.zeros(len(actions))

gamma = 0.9
threshold = 1e-6

#Two functions to convert representations of the player's position
def rc_to_index(row, col):
    return N * row + col

def index_to_rc(index):
    return index // N , index % N

def get_adjacent_cells(index):
    row, col = index_to_rc(index)
    neighbors = []

    if row > 0:  # Up
        neighbors.append(rc_to_index(row - 1, col))
    if row < M - 1:  # Down
        neighbors.append(rc_to_index(row + 1, col))
    if col > 0:  # Left
        neighbors.append(rc_to_index(row, col - 1))
    if col < N - 1:  # Right
        neighbors.append(rc_to_index(row, col + 1))

    return neighbors

def fire_spread_outcomes(fire_state, spread_prob):
    new_states = []
    spread_outcomes = [] 

    #Track total number of fires
    fire_match = 0
    for i in range(grid_size):
        if fire_state[i] == 1:
            fire_match += 1
    
    # List of fire-spread scenarios
    for spread_pattern in itertools.product([0, 1], repeat=grid_size):

        fire_count = 0
        fire_match_count = 0

        for i in range(grid_size):
            if fire_state[i] == 0 and spread_pattern[i] == 1:
                fire_count += 1
            elif fire_state[i] == 1 and spread_pattern[i] == 1:
                fire_match_count += 1
        
        if fire_count == 1 and fire_match_count == fire_match:
            spread_outcomes.append(tuple(spread_pattern))

    if len(spread_outcomes) > 0:
        for outcome in spread_outcomes:
            new_states.append((outcome, spread_prob/(grid_size-fire_match)))

    stay_prob = 1

    if fire_match < grid_size:
        stay_prob -= (spread_prob/(grid_size-fire_match) * len(spread_outcomes))
    
    new_states.append((fire_state, stay_prob))
    
    return new_states

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
        fire_spreads = fire_spread_outcomes(fire_state, fire_spread_prob)

        for spread_fire_state, prob in fire_spreads:
            next_states.append(((new_pos, tuple(spread_fire_state)), prob, reward))

    return next_states


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

# Print final Q(s,a) values
print("\nComputed Q(s,a) values:")
for state in states:
    print(f"State {state}: {Q[state]}")

#Print best action in each state
for state in states:
    if state in terminal_states:
        print(f"State {state}: Terminal")
    else:
        best_action_index = np.argmax(Q[state])  # Index of the max Q-value
        best_action = actions[best_action_index]  # Corresponding action
        print(f"State {state}: Best Action -> {best_action}")


