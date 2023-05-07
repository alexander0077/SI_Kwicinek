import random
import copy
from Game import Game
import math


class MonteCarloGameState:
    def __init__(self, curent_player, gmBoard: Game):
        self.visited = 0
        self.current_player = curent_player
        self.wins = 0
        self.children = []
        self.board = gmBoard
        # column_diffrence to ruch w jakiej kolumnie rozni dziecko od rodzica
        self.column_diffrence = -1


class MonteCarloTreeSearchAgent:
    def __init__(self, my_token=1, initial_iterations=1000, tradeOffConstant=2):
        self.my_token = my_token
        if my_token == 2:
            self.pNum = -1
        else:
            self.pNum = 1
        self.initial_iterations = int(initial_iterations)
        self.tradeOffConstant = tradeOffConstant

    def toString(self):
        return "MCTS\n[" + str(self.initial_iterations) + " iteracji]"
    def decide(self, board):
        root = MonteCarloGameState(self.pNum, board)
        for i in range(self.initial_iterations):
            self.alghoritm(root)
        if not root.children:
            # pelna plansza
            return -1
        # algorytm UCT
        UCTarr = []
        for child in root.children:
            weight = (child.visited-child.wins)/(child.visited + 0.001) + self.tradeOffConstant * (math.sqrt((math.log(root.visited) / (child.visited + 0.001))))
            UCTarr.append(weight)

        bestUCTidx = UCTarr.index(max(UCTarr))
        childToChoose = root.children[bestUCTidx]
        return childToChoose.column_diffrence

    def alghoritm(self, state: MonteCarloGameState):
        state.visited += 1
        for four in state.board.iter_fours():
            if four == [1, 1, 1, 1]:
                if state.current_player == 1:
                    state.wins += 1
                    return 1
            elif four == [2, 2, 2, 2]:
                if state.current_player == -1:
                    state.wins += 1
                    return -1
        pos_drops = state.board.possible_drops()
        if not pos_drops:
            state.wins += 0.5
            return 0

        if not state.children:
            # jesli nie ma dzieci
            for column in pos_drops:
                tmp = copy.deepcopy(state.board)
                tmp.dodajKrazek(column)
                child = MonteCarloGameState(state.current_player * -1, tmp)
                child.column_diffrence = column
                state.children.append(child)

        # uzywamy algorytmu UCT
        UCTarr = []
        for child in state.children:
            weight = child.wins/(child.visited + 0.001) + self.tradeOffConstant * (math.sqrt((math.log(state.visited) / (child.visited + 0.001))))
            UCTarr.append(weight)

        if not UCTarr:
            ble = 1
        firstElement = UCTarr[0]
        isEqual = True
        for ele in UCTarr:
            if ele != firstElement:
                isEqual = False

        if isEqual:
            childToChoose = random.choice(state.children)
        else:
            bestUCTidx = UCTarr.index(max(UCTarr))
            childToChoose = state.children[bestUCTidx]
        whoWins = self.alghoritm(childToChoose)
        if whoWins == 0:
            state.wins += 0.5
        elif whoWins == state.current_player:
            state.wins += 1
        return whoWins
