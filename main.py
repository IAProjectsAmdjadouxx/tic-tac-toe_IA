from environment import TicTacToeEnv
from agent import QLearningTicTacToeAgent

# def main_one():
#     env = TicTacToeEnv()
#     env.render(env.board)
#     while not env.done:
#         available_actions = env.get_available_actions()
#         print('Available actions:', available_actions)
#         action = int(input('Choose an action: '))
#         if action not in available_actions:
#             print('Invalid action')
#             continue
#         env.step(action)
#         env.render(env.board)
#     if env.winner:
#         print(f'{env.winner} wins!')
#     else:
#         print('It\'s a draw!')

def train():
    env = TicTacToeEnv()
    agent = QLearningTicTacToeAgent(alpha=0.1, gamma=0.9, epsilon=0.1)
    episodes = 1000

    for episode in range(episodes):
        state = env.reset()
        done = False

        while not done:
            action = agent.choose_action(state)
            next_state, reward, done = env.step(action)
            agent.update_q_value(state, action, reward, next_state)
            state = next_state

    agent.print_q_table()
    agent.save_q_table('q_table.pkl')

def play_vs_ia():
    env = TicTacToeEnv()
    agent = QLearningTicTacToeAgent(alpha=0.1, gamma=0.9, epsilon=0.1)
    agent.load_q_table('q_table.pkl')

    env.render(env.board)
    while not env.done:
        if env.current_player == 'O':
            available_actions = env.get_available_actions()
            print('Available actions:', available_actions)
            action = int(input('Choose an action: '))
            if action not in available_actions:
                print('Invalid action')
                continue
            env.step(action)
        else:
            action = agent.choose_action(env.board)
            env.step(action)
        env.render(env.board)
    if env.winner:
        print(f'{env.winner} wins!')
    else:
        print('It\'s a draw!')

if __name__ == '__main__':
    inpt = input('Train or play? (train/play): ')
    if inpt == 'train':
        train()
    elif inpt == 'play':
        play_vs_ia()
    else:
        print('Invalid option')