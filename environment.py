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

    def get_reward(self):
        if self.winner == 'X':
            return 1
        if self.winner == 'O':
            return -1
        return 0

    def check_winner(self):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                                (0, 3, 6), (1, 4, 7), (2, 5, 8),
                                (0, 4, 8), (2, 4, 6)]
        for i, j, k in winning_combinations:
            if self.board[i] == self.board[j] == self.board[k] != ' ':
                self.winner = self.board[i]
                return True
        return False

    def is_done(self):
        if ' ' not in self.board:
            return True
        return self.check_winner()

    def get_available_actions(self):
        return [i for i, x in enumerate(self.board) if x == ' ']

    def step(self, action):
        if self.board[action] == ' ':
            self.board[action] = self.current_player
            self.done = self.is_done()
            if not self.done:
                self.current_player = 'X' if self.current_player == 'O' else 'O'
        return self.board, self.get_reward(), self.done
