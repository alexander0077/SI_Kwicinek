import random
import copy


class MinMaxABAgent:
    def __init__(self, my_token=1, initial_depth=6):
        self.my_token = my_token
        if my_token == 2:
            self.pNum = -1
        else:
            self.pNum = 1
        self.initial_depth = initial_depth

    def toString(self):
        return "AlfaBeta [głębokość " + str(self.initial_depth) + "]"
    def decide(self, connect4):
        pos_drops = connect4.possible_drops()
        if not pos_drops:
            return None
        results = []
        for drop in pos_drops:
            tmp = copy.deepcopy(connect4)
            tmp.dodajKrazek(drop)
            results.append(self.minmax(tmp, self.pNum, 6, -1000, 1000))
        allEquall = True
        ele = results[0]
        for i in results:
            if i != ele:
                allEquall = False
                break
        if allEquall:
            return random.choice(pos_drops)
        if self.pNum == -1:
            max_index = results.index(max(results))
            return pos_drops[max_index]
        else:
            min_index = results.index(min(results))
            return pos_drops[min_index]

    def minmax(self, connect4, maximizingPlayer, glebia, alpha, beta):
        if glebia == 0:
            return 0
        pos_drops = connect4.possible_drops()
        for four in connect4.iter_fours():
            if four == [1, 1, 1, 1]:
                return -1
            elif four == [2, 2, 2, 2]:
                return 1
        if not pos_drops:
            return 0

        if maximizingPlayer == 1:
            value = -1000
            for board in pos_drops:
                tmp = copy.deepcopy(connect4)
                tmp.dodajKrazek(board)
                value = max(value, self.minmax(tmp, maximizingPlayer * -1, glebia - 1, alpha, beta))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = 1000
            for board in pos_drops:
                tmp2 = copy.deepcopy(connect4)
                tmp2.dodajKrazek(board)
                value = min(value, self.minmax(tmp2, maximizingPlayer * -1, glebia - 1, alpha, beta))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value
