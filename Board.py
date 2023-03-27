from tkinter import Tk
import tkinter as tk

class Board:
    __CELLS = list()
    __TURN_1 = True

    def __init__(self):
        self.__CELLS = [[0 for _ in range(7)] for _ in range(6)]

    def getCells(self):
        return self.__CELLS
    def ifLast(self):
        return True

    def addCoin(self, i):
        iterator = 0
        while self.__CELLS[iterator][i] != 0:
            iterator += 1

        if self.__TURN_1:
            self.__CELLS[iterator][i] = 1
        else:
            self.__CELLS[iterator][i] = -1
        self.__TURN_1 = not self.__TURN_1