import random
import pickle

class QLearningTicTacToeAgent:
    def __init__(self, alpha, gamma, epsilon):
        self.q_table = {}
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def choose_action(self, state):
        state_str = str(state)
        if state_str not in self.q_table:
            self.q_table[state_str] = [0] * 9
        if random.uniform(0, 1) < self.epsilon:
            return random.choice([i for i, x in enumerate(state) if x == ' '])
        return max(range(9), key=lambda x: self.q_table[state_str][x] if state[x] == ' ' else -float('inf'))

    def update_q_value(self, state, action, reward, next_state):
        state_str = str(state)
        next_state_str = str(next_state)
        if state_str not in self.q_table:
            self.q_table[state_str] = [0] * 9
        if next_state_str not in self.q_table:
            self.q_table[next_state_str] = [0] * 9
        
        best_next_action_value = max(self.q_table[next_state_str])
        current_q_value = self.q_table[state_str][action]
        new_q_value = current_q_value + self.alpha * (reward + self.gamma * best_next_action_value - current_q_value)
        self.q_table[state_str][action] = new_q_value
        
        # Debug statement to verify the update
        print(f"Updated Q-value for state {state_str}, action {action}: {new_q_value}, reward: {reward}, best_next_action_value: {best_next_action_value}")

    def print_q_table(self):
        for state, actions in self.q_table.items():
            print(state)
            print(actions)

    def save_q_table(self, file_name):
        with open(file_name, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, file_name):
        with open(file_name, 'rb') as f:
            self.q_table = pickle.load(f)