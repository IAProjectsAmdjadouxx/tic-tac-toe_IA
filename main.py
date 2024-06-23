import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Flatten, concatenate
import os
from tensorflow.keras.callbacks import TensorBoard
from time import time

#rm log dir
list_file = os.listdir()
if "logs" in list_file:
    os.remove("./logs")
tensorboard = TensorBoard(log_dir="logs".format(time()))

NAME_AI = "TTT_model"
EPOCHS = 90

class TicTacToeDataGenerator:
    @staticmethod
    def generate_data(num_samples):
        X_board, X_player, y = [], [], []

        for _ in range(num_samples):
            board = np.random.choice([0, 1, 2], size=(3, 3))
            player = np.random.choice([1, 2])
            possible_moves = np.argwhere(board == 0)

            if possible_moves.size > 0:
                move = possible_moves[np.random.choice(len(possible_moves))]
                X_board.append(board)
                X_player.append(player)
                y.append(move[0] * 3 + move[1])

        return np.array(X_board), np.array(X_player).reshape(-1, 1), np.array(y)

class TicTacToeModel:
    def __init__(self):
        self.model = self._build_model()

    def _build_model(self):
        input_board = Input(shape=(3, 3), name='input_board')
        flatten_board = Flatten()(input_board)
        input_player = Input(shape=(1,), name='input_player')
        combined = concatenate([flatten_board, input_player])
        z = Dense(128, activation='relu')(combined)
        z = Dense(64, activation='relu')(z)
        output = Dense(9, activation='softmax')(z)
        model = Model(inputs=[input_board, input_player], outputs=output)
        return model

    def compile(self):
        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

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
        num_samples = 1000
        data_generator = TicTacToeDataGenerator()
        X_board, X_player, y = data_generator.generate_data(num_samples)
        tic_tac_toe_model = TicTacToeModel()
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