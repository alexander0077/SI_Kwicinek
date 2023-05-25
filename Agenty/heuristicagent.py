import copy
import numpy as np


class StaticAgent:
    def __init__(self, my_token=1):
        self.my_token = my_token
        self.opponent_token = 3 - my_token

    def toString(self):
        return "Heurystyka statyczna"

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
        num_fours_agent1 = 0
        num_fours_agent2 = 0
        for sequence in game.iter_fours():
            if sequence.count(self.my_token) == 4:
                num_fours_agent1 += 10
            elif sequence.count(self.opponent_token) == 4:
                num_fours_agent2 += 10
            elif sequence.count(self.my_token) == 3 and sequence.count(0) == 1:
                num_fours_agent1 += 0.8
            elif sequence.count(self.opponent_token) == 3 and sequence.count(0) == 1:
                num_fours_agent2 += 0.8
            elif sequence.count(self.my_token) == 2 and sequence.count(0) == 2:
                num_fours_agent1 += 0.3
            elif sequence.count(self.opponent_token) == 2 and sequence.count(0) == 2:
                num_fours_agent2 += 0.3
            elif sequence.count(self.my_token) == 1 and sequence.count(0) == 3:
                num_fours_agent1 += 0.2
            elif sequence.count(self.opponent_token) == 1 and sequence.count(0) == 3:
                num_fours_agent2 += 0.2

        target = num_fours_agent1 - num_fours_agent2
        return target