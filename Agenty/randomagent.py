import random
import copy


class RandomAgent:
    def __init__(self, my_token=1):
        self.my_token = my_token
        if my_token == 2:
            self.pNum = -1
        else:
            self.pNum = 1

    def toString(self):
        return "Random Agent"
    def decide(self, connect4):
        pos_drops = connect4.possible_drops()
        if not pos_drops:
            return None

        return random.choice(pos_drops)