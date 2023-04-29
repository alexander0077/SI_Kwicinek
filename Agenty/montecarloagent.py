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
    def __init__(self, my_token=1, initial_iterations=1000, tradeOffConstant=8):
        self.my_token = my_token
        if my_token == 2:
            self.pNum = -1
        else:
            self.pNum = 1
        self.initial_iterations = initial_iterations
        self.tradeOffConstant = tradeOffConstant

    # TODO implement decide method

    def alghoritm(self, state: MonteCarloGameState):
        state.visited += 1
        for four in state.board.iter_fours():
            if four == [1, 1, 1, 1]:
                if state.current_player == 1:
                    state.wins += 1
                    return 1
            elif four == [2, 2, 2, 2]:
                if state.current_player == 2:
                    state.wins += 1
                    return 2
        pos_drops = state.board.possible_drops()
        if pos_drops is None:
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
            weight = child.wins + self.tradeOffConstant * (math.sqrt((math.log(state.visited) / (child.visited + 0.5))))
            UCTarr.append(weight)

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
