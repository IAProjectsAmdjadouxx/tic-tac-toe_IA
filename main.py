import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Flatten, concatenate, Dropout
import os
from tensorflow.keras.callbacks import TensorBoard
from time import time

#rm log dir
list_file = os.listdir()

NAME_AI = "TTT_model"
EPOCHS = 10

class TicTacToeDataGenerator:
    @staticmethod
    def generate_data(num_samples):
        X_board, X_player, y = [], [], []
        i = 0

        while i < num_samples:
            board = np.random.choice([0, 1, 2], size=(3, 3))
            player = np.random.choice([1, 2])
            possible_moves = np.argwhere(board == 0)

            if possible_moves.size > 0:
                move = TicTacToeDataGenerator.minimax(board, player)
                is_in = False
                for j in range(len(X_player)):
                    if np.array_equal(X_board[j], board) and X_player[j] == player and y[j] == move[0] * 3 + move[1]:
                        is_in = True
                        break
                if is_in:
                    continue
                X_board.append(board)
                X_player.append(player)
                y.append(move[0] * 3 + move[1])
                print(f"Generated {i + 1}/{num_samples} samples:\n {board}, {player}, {move}")
                i += 1

        return np.array(X_board), np.array(X_player).reshape(-1, 1), np.array(y)

    @staticmethod
    def minimax(board, player):
        def is_winner(board, player):
            for i in range(3):
                if np.all(board[i, :] == player) or np.all(board[:, i] == player):
                    return True
            if np.all(np.diag(board) == player) or np.all(np.diag(np.fliplr(board)) == player):
                return True
            return False

        def minimax_helper(board, player, depth, is_maximizing):
            opponent = 1 if player == 2 else 2
            if is_winner(board, player):
                return 10 - depth
            elif is_winner(board, opponent):
                return depth - 10
            elif not np.any(board == 0):
                return 0

            if is_maximizing:
                best_score = -np.inf
                for move in np.argwhere(board == 0):
                    board[move[0], move[1]] = player
                    score = minimax_helper(board, player, depth + 1, False)
                    board[move[0], move[1]] = 0
                    best_score = max(score, best_score)
                return best_score
            else:
                best_score = np.inf
                for move in np.argwhere(board == 0):
                    board[move[0], move[1]] = opponent
                    score = minimax_helper(board, player, depth + 1, True)
                    board[move[0], move[1]] = 0
                    best_score = min(score, best_score)
                return best_score

        best_move = None
        best_score = -np.inf
        for move in np.argwhere(board == 0):
            board[move[0], move[1]] = player
            score = minimax_helper(board, player, 0, False)
            board[move[0], move[1]] = 0
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

class TicTacToeModel:
    def __init__(self):
        self.model = self._build_model()

    def _build_model(self):
        input_board = Input(shape=(3, 3), name='input_board')
        flatten_board = Flatten()(input_board)
        input_player = Input(shape=(1,), name='input_player')
        combined = concatenate([flatten_board, input_player])
        dense_1 = Dense(64, activation='relu')(combined)
        dropout_1 = Dropout(0.5)(dense_1)
        dense_2 = Dense(32, activation='relu')(dropout_1)
        dropout_2 = Dropout(0.5)(dense_2)
        output = Dense(9, activation='linear')(dropout_2)
        model = Model(inputs=[input_board, input_player], outputs=output)
        return model

    def compile(self):
        self.model.compile(optimizer='adam', loss='crossentropy', metrics=['accuracy'])

    def train(self, X_board, X_player, y, epochs=50, batch_size=32, validation_split=0.2):
        self.model.fit([X_board, X_player], y, epochs=epochs, batch_size=batch_size, validation_split=validation_split, callbacks=[tensorboard])

    def save(self, path):
        self.model.save(path)

    def predict_move(self, board, player):
        board = board.reshape((1, 3, 3))
        player = player.reshape((1, 1))
        predictions = self.model.predict([board, player])
        best_move = np.argmax(predictions)
        return best_move // 3, best_move % 3

if __name__ == "__main__":
    files = os.listdir()

    if NAME_AI + ".keras" not in files:
        if "logs" in list_file:
            os.system("rm -rf logs")
        tensorboard = TensorBoard(log_dir="logs".format(time()))
        num_samples = 250
        data_generator = TicTacToeDataGenerator()
        X_board, X_player, y = data_generator.generate_data(num_samples)
        tic_tac_toe_model = TicTacToeModel()
        tic_tac_toe_model.model.summary()
        tic_tac_toe_model.compile()
        tic_tac_toe_model.train(X_board, X_player, y, EPOCHS)
        tic_tac_toe_model.save(NAME_AI + ".keras")

    tic_tac_toe_model = TicTacToeModel()
    while True:
        tab_tic_tac_toe = input("Entrez le tableau de jeu (0 pour les cases vides, 1 pour les cases du joueur 1 et 2 pour les cases du joueur 2) : ")
        assert len(tab_tic_tac_toe) == 9, "Le tableau doit contenir 9 cases"
        tab_tic_tac_toe = np.array([int(i) for i in tab_tic_tac_toe]).reshape((3, 3))
        print(tab_tic_tac_toe)
        player = int(input("Entrez le joueur (1 ou 2) : "))
        best_move = tic_tac_toe_model.predict_move(tab_tic_tac_toe, np.array([player]))
        print(f"Le meilleur coup est : {best_move[0]}, {best_move[1]}")