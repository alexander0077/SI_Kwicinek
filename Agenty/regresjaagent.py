import copy

import numpy as np

from Game import Game


class RegresjaAgent:
    def __init__(self, my_token=1, weights=None):
        self.my_token = my_token
        if my_token == 2:
            self.pNum = -1
        else:
            self.pNum = 1
        self.weights = weights if weights is not None else [1, 1, 1, 1, 1, 1, 1]

    def toString(self):
        return "Linear Regression"

    def decide(self, game):
        pos_drops = game.possible_drops()
        if not pos_drops:
            return None
        best_drop = pos_drops[0]
        best_evaluation = float('-inf')

        for drop in pos_drops:
            tmp = copy.deepcopy(game)
            tmp.dodajKrazek(drop)
            evaluation = self.evaluate(tmp)

            if evaluation > best_evaluation:
                best_evaluation = evaluation
                best_drop = drop

        return best_drop

    def evaluate(self, game):
        feature_vector = self.get_feature_vector(game)
        evaluation = sum(w * f for w, f in zip(self.weights, feature_vector))
        return evaluation

    def get_feature_vector(self, game):
        feature_vector = []
        for player in [self.my_token, 3 - self.my_token]:
            for length in [2, 3, 4]:
                count = self.get_sequences_count(game, player, length)
                feature_vector.append(count)
            # Dodawanie cech wyższego rzędu
            feature_vector.append(feature_vector[-1] * feature_vector[-2])
            feature_vector.append(feature_vector[-2] * feature_vector[-3])
        return feature_vector

    def get_feature_vector_from_state(self, state):
        game = Game()
        game.set_board_state(state)
        return self.get_feature_vector(game)

    def get_sequences_count(self, game, player, length):
        count = 0
        for sequence in game.iter_sequences(length):
            if all(token == player for token in sequence):
                count += 1
        return count

    def train(self, training_data):
        X = np.array([self.get_feature_vector_from_state(state) for state, _ in training_data])
        y = np.array([target for _, target in training_data])

        X_pseudo_inverse = np.linalg.pinv(X)
        self.weights = X_pseudo_inverse.dot(y)

    def get_threat_count(self, game, player):
        threat_count = 0
        for sequence in game.iter_sequences(4):  # Zakładając, że potrzebujemy 4 tokeny w linii, aby wygrać
            empty_count = sequence.count(0)
            player_count = sequence.count(player)
            if empty_count == 1 and player_count == 3:  # Zagrożenie występuje, gdy są 3 tokeny gracza i jedno puste miejsce
                threat_count += 1
        return threat_count

