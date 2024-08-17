from environment import TicTacToeEnv

def main():
    env = TicTacToeEnv()
    env.render(env.board)
    while not env.done:
        available_actions = env.get_available_actions()
        print('Available actions:', available_actions)
        action = int(input('Choose an action: '))
        if action not in available_actions:
            print('Invalid action')
            continue
        env.step(action)
        env.render(env.board)
    if env.winner:
        print(f'{env.winner} wins!')
    else:
        print('It\'s a draw!')

if __name__ == '__main__':
    main()