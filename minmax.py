def minMaxChecker(board, player):
    opponent = 'O' if player == 'X' else 'X'

    def is_winner(board, player):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
                return True
        return False

    def is_draw(board):
        return ' ' not in board

    def minimax(board, depth, is_maximizing):
        if is_winner(board, player):
            return 1
        if is_winner(board, opponent):
            return -1
        if is_draw(board):
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = player
                    score = minimax(board, depth + 1, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = opponent
                    score = minimax(board, depth + 1, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    best_move = None
    best_score = -float('inf')
    for i in range(9):
        if board[i] == ' ':
            board[i] = player
            score = minimax(board, 0, False)
            board[i] = ' '
            if score > best_score:
                best_score = score
                best_move = i

    return best_move
