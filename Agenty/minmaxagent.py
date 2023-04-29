import random
import copy


class MinMaxAgent:
    def __init__(self, my_token=1, initial_depth=3):
        self.my_token = my_token
        if my_token == 2:
            self.pNum = -1
        else:
            self.pNum = 1
        self.initial_depth = initial_depth

    def decide(self, connect4):
        pos_drops = connect4.possible_drops()
        results = []
        for drop in pos_drops:
            tmp = copy.deepcopy(connect4)
            tmp.dodajKrazek(drop)
            results.append(self.minmax(tmp, self.pNum, self.initial_depth))
        isZero = False
        zeroTab = []
        for i in range(len(results)):
            if self.pNum == -1:
                if results[i] == 1:
                    return pos_drops[i]
                elif results[i] == 0:
                    isZero = True
                    zeroTab.append(pos_drops[i])
            else:
                if results[i] == -1:
                    return pos_drops[i]
                elif results[i] == 0:
                    isZero = True
                    zeroTab.append(pos_drops(i))
        if isZero:
            return random.choice(zeroTab)
        else:
            return random.choice(pos_drops)

    def minmax(self, connect4, maximizingPlayer, glebia):
        if glebia == 0:
            return 0
        pos_drops = connect4.possible_drops()
        if not pos_drops:
            for four in connect4.iter_fours():
                if four == [1, 1, 1, 1]:
                    return -1
                elif four == [2, 2, 2, 2]:
                    return 1
            return 0
        for four in connect4.iter_fours():
            if four == [1, 1, 1, 1]:
                return -1
            elif four == [2, 2, 2, 2]:
                return 1

        if maximizingPlayer == 1:
            value = -1000
            for board in pos_drops:
                tmp = copy.deepcopy(connect4)
                tmp.dodajKrazek(board)
                value = max(value, self.minmax(tmp, maximizingPlayer * -1, glebia - 1))
            return value
        else:
            value = 1000
            for board in pos_drops:
                tmp2 = copy.deepcopy(connect4)
                tmp2.dodajKrazek(board)
                value = min(value, self.minmax(tmp2, maximizingPlayer * -1, glebia - 1))
            return value
