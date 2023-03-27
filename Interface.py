from tkinter import Tk
from Board import Board
import tkinter as tk
from Game import Game


class Interface:
    __SZEROKOSC_EKRANU = 900
    __WYSOKOSC_EKRANU = 600
    __SZEROKOSC_PRZYCISKU_MENU = 40
    __ODLEGLOSC_OD_PRAWEJ_KRAWEDZI_PRZYCISKU_MENU = 310
    __BACKGROUD_COLOR = '#adad9a'
    __BUTTONS_COLOR = '#d1c75a'
    __WYSOKOSC_PRZYCISKU = 4

    __NONE = 99
    __GORA = 101
    __DOL = 102
    __PRAWO = 103
    __LEWO = 104

    screen = None
    game = None

    def __init__(self):
        self.game = Game()
        self.screen = Tk()
        self.screen.title('4 w linii')
        self.screen.geometry(str(self.__SZEROKOSC_EKRANU) + "x" + str(self.__WYSOKOSC_EKRANU))
        self.screen.resizable(False, False)
        self.mainMenu()

    def mainMenu(self):  # GLOWNY INTERFACE Z WYBOREM TRYBU I WYJSCIEM
        for widgets in self.screen.winfo_children():
            widgets.destroy()
        self.screen.configure(bg=self.__BACKGROUD_COLOR)

        game_title = tk.Label(self.screen, text="Connect 4", font=('Arial', 32))
        game_title.place(relx=0.5, rely=0.04, anchor='n')
        game_title.configure(bg=self.__BACKGROUD_COLOR)
        game_title.configure(anchor='center')

        button_BOT = tk.Button(self.screen, text="Graj przeciwko SI", fg="black",
                               command=lambda: self.graBOT(),
                               height=self.__WYSOKOSC_PRZYCISKU, width=self.__SZEROKOSC_PRZYCISKU_MENU,
                               bg=self.__BUTTONS_COLOR)
        button_BOT.place(x=self.__ODLEGLOSC_OD_PRAWEJ_KRAWEDZI_PRZYCISKU_MENU, y=125)

        button_1v1 = tk.Button(self.screen, text="Gra na 2 graczy", fg="black", command=lambda: self.gra1v1(),
                               height=self.__WYSOKOSC_PRZYCISKU, width=self.__SZEROKOSC_PRZYCISKU_MENU,
                               bg=self.__BUTTONS_COLOR)
        button_1v1.place(x=self.__ODLEGLOSC_OD_PRAWEJ_KRAWEDZI_PRZYCISKU_MENU, y=225)

        button_wyjdz = tk.Button(self.screen, text="Wyjdź", fg="black", command=quit, height=self.__WYSOKOSC_PRZYCISKU,
                                 width=self.__SZEROKOSC_PRZYCISKU_MENU, bg=self.__BUTTONS_COLOR)
        button_wyjdz.place(x=self.__ODLEGLOSC_OD_PRAWEJ_KRAWEDZI_PRZYCISKU_MENU, y=375)

        self.screen.mainloop()

    def clear_window(self):
        for widgets in self.screen.winfo_children():
            widgets.destroy()

    def printBoard(self):
        board_rows = 6
        board_cols = 7
        canvas_width = 400
        canvas_height = 500
        cell_size = 40
        cell_padding = 5

        canvas = tk.Canvas(self.screen, width=canvas_width, height=canvas_height)
        canvas.configure(bg=self.__BACKGROUD_COLOR)
        canvas.pack()

        board_width = board_cols * (cell_size + cell_padding) - cell_padding
        board_height = board_rows * (cell_size + cell_padding) - cell_padding
        board_x = (canvas_width - board_width) // 2
        board_y = (canvas_height - board_height) // 2

        # draw the game board on the canvas
        x1 = 20
        y2 = 20
        for row in range(board_rows):
            for col in range(board_cols):
                # calculate the coordinates of the cell
                x1 = board_x + col * (cell_size + cell_padding)
                y1 = board_y + row * (cell_size + cell_padding)
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                # draw the cell
                tmp = self.game.getArr()
                if tmp[row][col] == 0:
                    canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')
                elif tmp[row][col] == 1:
                    canvas.create_rectangle(x1, y1, x2, y2, fill='blue', outline='black')
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, fill='red', outline='black')

        for i in range(board_cols):
            button = tk.Button(self.screen, text="  ", command=lambda i=i: self.move(i),
                               height=2, width=5)
            button.place(x=x1 - (cell_size + cell_padding) / 2 + i * (cell_size + cell_padding), y=y2 + 20)

    def graBOT(self, ):  # TODO TU BEDZIE CALY PROJEKT TAK W SUMIE
        print("bot")

    def move(self, i):
        stan = self.game.dodajKrazek(i)
        if stan == 11:
            print("Wygral gracz 1")
        elif stan == 12:
            print("Wygral gracz 2")
        self.clear_window()
        self.printBoard()

    def gra1v1(self):
        board = Board()
        self.clear_window()
        while board.ifLast():
            self.clear_window()
            self.printBoard()
            break
