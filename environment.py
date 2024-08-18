from minmax import minMaxChecker

class TicTacToeEnv:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.done = False
        self.winner = None

    def render(self, board):
        print('-------------')
        print('| ' + ' | '.join(board[:3]) + ' |')
        print('-------------')
        print('| ' + ' | '.join(board[3:6]) + ' |')
        print('-------------')
        print('| ' + ' | '.join(board[6:]) + ' |')
        print('-------------')

    def reset(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.done = False
        self.winner = None
        return self.board

    #determine if its the best move with minmax
    def get_reward(self, best_move_to_do, action):
        if best_move_to_do == action:
            return 1
        return -1

    def check_winner(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                self.winner = self.board[combo[0]]
                return True
        return False

    def is_done(self):
        if ' ' not in self.board:
            return True
        return self.check_winner()

    def get_available_actions(self):
        return [i for i, x in enumerate(self.board) if x == ' ']

    def step(self, action):
        best_move = minMaxChecker(self.board, self.current_player)
        if self.board[action] == ' ':
            self.board[action] = self.current_player
            self.done = self.is_done()
            if not self.done:
                self.current_player = 'X' if self.current_player == 'O' else 'O'
        return self.board, self.get_reward(best_move, action), self.done
