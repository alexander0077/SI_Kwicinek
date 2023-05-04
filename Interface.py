import time
from tkinter import Tk
from tkinter import ttk
from Agenty.alphabetaagent import MinMaxABAgent
from Agenty.montecarloagent import MonteCarloTreeSearchAgent
from Board import Board
import tkinter as tk
from Game import Game
from Agenty.minmaxagent import MinMaxAgent


class Interface:
    __ZAIMPLEMENTOWANE_BOTY = [
        "MinMax",
        "AlphaBeta",
        "MonteCarloTreeSearch"
    ]
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

    instancjaBota1 = None
    instancjaBota2 = None

    screen = None
    game = None
    wygraneBot1 = 0
    wygraneBot2 = 0

    def __init__(self):
        self.game = Game()
        self.screen = Tk()
        self.bot1 = tk.StringVar(self.screen)
        self.bot1.set(self.__ZAIMPLEMENTOWANE_BOTY[0])
        self.bot1_value = 3  # wartosc bota 1: glebokosc/iteracje
        self.bot2 = tk.StringVar(self.screen)
        self.bot2.set(self.__ZAIMPLEMENTOWANE_BOTY[0])
        self.bot2_value = 3  # wartosc bota 2: glebokosc/iteracje
        self.screen.title('4 w linii')
        self.screen.geometry(str(self.__SZEROKOSC_EKRANU) + "x" + str(self.__WYSOKOSC_EKRANU))
        self.screen.resizable(False, False)
        self.lastWinTime = 0
        self.last_winner = "Remis"
        self.mainMenu()


    def mainMenu(self):  # GLOWNY INTERFACE Z WYBOREM TRYBU I WYJSCIEM
        for widgets in self.screen.winfo_children():
            widgets.destroy()
        self.screen.configure(bg=self.__BACKGROUD_COLOR)

        game_title = tk.Label(self.screen, text="Connect 4", font=('Arial', 32))
        game_title.place(relx=0.5, rely=0.04, anchor='n')
        game_title.configure(bg=self.__BACKGROUD_COLOR)
        game_title.configure(anchor='center')

        button_BOT = tk.Button(self.screen, text="Gra SI vs SI", fg="black",
                               command=lambda: self.graBotInterface(),
                               height=self.__WYSOKOSC_PRZYCISKU, width=self.__SZEROKOSC_PRZYCISKU_MENU,
                               bg=self.__BUTTONS_COLOR)
        button_BOT.place(x=self.__ODLEGLOSC_OD_PRAWEJ_KRAWEDZI_PRZYCISKU_MENU, y=125)

        button_1v1 = tk.Button(self.screen, text="Gra przeciwko SI", fg="black", command=lambda: self.gra1v1Interface(),
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
        canvas_height = 400
        cell_size = 40
        cell_padding = 5

        label = tk.Label(self.screen, text="", font=("Arial", 25), bg=self.__BACKGROUD_COLOR)

        if self.lastWinTime + 1 > time.time():
            label = tk.Label(self.screen, text=self.last_winner, font=("Arial", 25), bg=self.__BACKGROUD_COLOR)

        label.pack()


        player_1_canvas = tk.Canvas(self.screen, width=(self.__SZEROKOSC_EKRANU - canvas_width) / 2,
                                    height=canvas_height, highlightthickness=0)
        player_1_canvas.configure(bg=self.__BACKGROUD_COLOR)
        player_1_canvas.pack(side="left", padx=0, pady=0)

        player_1_canvas.create_text((self.__SZEROKOSC_EKRANU - canvas_width) / 4, 70, text='PLAYER 1:',
                                    font=("Arial", 16))
        player_1_canvas.create_text((self.__SZEROKOSC_EKRANU - canvas_width) / 4, 150,
                                    text=self.instancjaBota1.toString() + "\n",
                                    font=("Arial", 16))

        player_1_canvas.create_text((self.__SZEROKOSC_EKRANU - canvas_width) / 4, 160,
                                    text="wygrane:",
                                    font=("Arial", 16))

        player_1_canvas.create_text((self.__SZEROKOSC_EKRANU - canvas_width) / 4, 185,
                                    text=str(self.wygraneBot1),
                                    font=("Arial", 20))

        square_size = 30
        player_1_canvas.create_rectangle(((self.__SZEROKOSC_EKRANU - canvas_width) / 4) - square_size,
                                         (canvas_height / 2) - square_size + 40,
                                         ((self.__SZEROKOSC_EKRANU - canvas_width) / 4) + square_size,
                                         (canvas_height / 2) + square_size + 40,
                                         fill='blue', outline='black')

        canvas = tk.Canvas(self.screen, width=canvas_width, height=canvas_height, highlightthickness=0)
        canvas.configure(bg=self.__BACKGROUD_COLOR)
        canvas.pack(side="left")

        player_2_canvas = tk.Canvas(self.screen, width=(self.__SZEROKOSC_EKRANU - canvas_width) / 2,
                                    height=canvas_height, highlightthickness=0)
        player_2_canvas.configure(bg=self.__BACKGROUD_COLOR)
        player_2_canvas.pack(side="left", padx=0, pady=0)

        player_2_canvas.create_text((self.__SZEROKOSC_EKRANU - canvas_width) / 4, 70, text='PLAYER 2:',
                                    font=("Arial", 16))

        player_2_canvas.create_text((self.__SZEROKOSC_EKRANU - canvas_width) / 4, 150,
                                    text=self.instancjaBota2.toString() + "\n",
                                    font=("Arial", 16))

        player_2_canvas.create_text((self.__SZEROKOSC_EKRANU - canvas_width) / 4, 160,
                                    text="wygrane:",
                                    font=("Arial", 16))

        player_2_canvas.create_text((self.__SZEROKOSC_EKRANU - canvas_width) / 4, 185,
                                    text=str(self.wygraneBot2),
                                    font=("Arial", 20))

        square_size = 30
        player_2_canvas.create_rectangle(((self.__SZEROKOSC_EKRANU - canvas_width) / 4) - square_size,
                                         (canvas_height / 2) - square_size + 40,
                                         ((self.__SZEROKOSC_EKRANU - canvas_width) / 4) + square_size,
                                         (canvas_height / 2) + square_size + 40,
                                         fill='red', outline='black')

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
            button.place(x=x1 + 2 - (cell_size + cell_padding) / 2 + i * (cell_size + cell_padding), y=y2 + 130)



        h = self.__WYSOKOSC_EKRANU - (self.__WYSOKOSC_EKRANU - canvas_height) / 4 - 10

        return_button = tk.Button(self.screen, text="Powrót", fg="black", command=lambda: self.mainMenu(),
                                  height=2, width=15)
        return_button.place(x=self.__SZEROKOSC_EKRANU / 2 - 50, y=h)


    def boardNotFull(self):
        moves = self.game.possible_drops()

        if not moves:
            return False
        return True

    def graBOT(self, v1, v2):  # TODO TU BEDZIE CALY PROJEKT TAK W SUMIE
        if self.bot1.get() == "MinMax":
            self.instancjaBota1 = MinMaxAgent(1, int(v1))
        elif self.bot1.get() == "AlphaBeta":
            self.instancjaBota1 = MinMaxABAgent(1, int(v1))
        elif self.bot1.get() == "MonteCarloTreeSearch":
            self.instancjaBota1 = MonteCarloTreeSearchAgent(1, int(v1), 0.95)
        if self.bot2.get() == "MinMax":
            self.instancjaBota2 = MinMaxAgent(2, int(v2))
        elif self.bot2.get() == "AlphaBeta":
            self.instancjaBota2 = MinMaxABAgent(2, int(v2))
        elif self.bot2.get() == "MonteCarloTreeSearch":
            self.instancjaBota2 = MonteCarloTreeSearchAgent(2, int(v2), 0.95)
        # MIEJSCE NA INNE BOTY, TRZEBA JE BEDZIE ZAINICJALIZOWAC WZGLEDEM WYBORU UZYTKOWNIKA Z DROP DOWN MENU
        board = Board()
        self.clear_window()
        if not self.boardNotFull():
            self.last_winner = "Remis"
        while self.game.wining_player == -1 and self.boardNotFull():
            self.clear_window()
            self.printBoard()
            self.game.dodajKrazek(self.instancjaBota1.decide(self.game))
            self.clear_window()
            self.printBoard()
            self.screen.update_idletasks()
            self.screen.update()
            self.game.dodajKrazek(self.instancjaBota2.decide(self.game))
            self.clear_window()
            self.printBoard()
            if self.game.wining_player == 1:
                self.wygraneBot1 += 1
                self.last_winner = "Wygrywa: " + self.instancjaBota1.toString()
            elif self.game.wining_player == 2:
                self.last_winner = "Wygrywa: " + self.instancjaBota2.toString()
                self.wygraneBot2 += 1
            elif self.game.wining_player == 0:
                self.wygraneBot1 += 0.5
                self.wygraneBot2 += 0.5
            self.screen.update_idletasks()
            self.screen.update()

        print("")
        print(self.last_winner)

        self.lastWinTime = time.time()
        self.printBoard()


        print(self.instancjaBota1.toString() + " wygrane: " + str(self.wygraneBot1))
        print(self.instancjaBota2.toString() + " wygrane: " + str(self.wygraneBot2))
        self.game = Game()
        self.graBOT(v1, v2)

    def graBotInterface(self):
        self.clear_window()
        self.screen.configure(bg=self.__BACKGROUD_COLOR)

        # canvas do wyboru botow
        self.bot_choose_canvas = tk.Canvas(self.screen, width=300, height=200, bg=self.__BACKGROUD_COLOR,
                                           highlightthickness=0)
        self.bot_choose_canvas.pack(side="top", anchor="center", pady=50)

        def changeTagsBot1(screen):
            if self.bot1.get() == self.__ZAIMPLEMENTOWANE_BOTY[0] or self.bot1 == self.__ZAIMPLEMENTOWANE_BOTY[1]:
                label_bot_1_tag.config(text="   Głębkość ")

            if self.bot1.get() == self.__ZAIMPLEMENTOWANE_BOTY[2]:
                label_bot_1_tag.config(text="   Ilość iteracji: ")

        def changeTagsBot2(screen):
            if self.bot2.get() == self.__ZAIMPLEMENTOWANE_BOTY[0] or self.bot2 == self.__ZAIMPLEMENTOWANE_BOTY[1]:
                label_bot_2_tag.config(text="   Głębkość ")

            if self.bot2.get() == self.__ZAIMPLEMENTOWANE_BOTY[2]:
                label_bot_2_tag.config(text="   Ilość iteracji: ")

        # Wybor bota 1
        label1 = tk.Label(self.bot_choose_canvas, text="BOT 1: ", font=("Arial", 12), bg=self.__BACKGROUD_COLOR)
        label1.grid(row=0, column=0)
        bot_menu1 = tk.OptionMenu(self.bot_choose_canvas, self.bot1, *self.__ZAIMPLEMENTOWANE_BOTY,
                                  command=changeTagsBot1)
        bot_menu1.grid(row=0, column=1)
        label_bot_1_tag = tk.Label(self.bot_choose_canvas, text="   Głębkość ", font=("Arial", 12),
                                   bg=self.__BACKGROUD_COLOR)
        label_bot_1_tag.grid(row=0, column=2)
        self.bot1_value = tk.Entry(self.bot_choose_canvas)
        self.bot1_value.grid(row=0, column=3)

        # Wybor bot 2
        label2 = tk.Label(self.bot_choose_canvas, text="BOT 2: ", font=("Arial", 12), bg=self.__BACKGROUD_COLOR)
        label2.grid(row=1, column=0)
        bot_menu2 = tk.OptionMenu(self.bot_choose_canvas, self.bot2, *self.__ZAIMPLEMENTOWANE_BOTY,
                                  command=changeTagsBot2)
        bot_menu2.grid(row=1, column=1)
        label_bot_2_tag = tk.Label(self.bot_choose_canvas, text="   Głębkość ", font=("Arial", 12),
                                   bg=self.__BACKGROUD_COLOR)
        label_bot_2_tag.grid(row=1, column=2)
        self.bot2_value = tk.Entry(self.bot_choose_canvas)
        self.bot2_value.grid(row=1, column=3)

        start_button = tk.Button(self.screen, text="Rozpocznij gre", fg="black",
                                 command=lambda: self.graBOT(self.bot1_value.get(), self.bot2_value.get()),
                                 height=self.__WYSOKOSC_PRZYCISKU, width=self.__SZEROKOSC_PRZYCISKU_MENU,
                                 bg=self.__BUTTONS_COLOR)
        start_button.place(x=self.__ODLEGLOSC_OD_PRAWEJ_KRAWEDZI_PRZYCISKU_MENU, y=225)

        return_button = tk.Button(self.screen, text="Powrót", fg="black", command=lambda: self.mainMenu(),
                                  height=self.__WYSOKOSC_PRZYCISKU, width=self.__SZEROKOSC_PRZYCISKU_MENU,
                                  bg=self.__BUTTONS_COLOR)
        return_button.place(x=self.__ODLEGLOSC_OD_PRAWEJ_KRAWEDZI_PRZYCISKU_MENU, y=400)

    def move(self, i):
        if self.game.current_Player == 2:
            return
        self.game.dodajKrazek(i)
        # TODO dodac przerwanie gry i wyswietlenie kto wygral
        if self.game.wining_player == 1:
            print("Wygral gracz 1")
        elif self.game.wining_player == 2:
            print("Wygral gracz 2")
        elif self.game.wining_player == 0:
            print("Nastapil remis")
        self.clear_window()
        self.printBoard()
        self.game.dodajKrazek(self.instancjaBota1.decide(self.game))
        self.clear_window()
        self.printBoard()

    def gra1v1Interface(self):
        self.clear_window()
        self.screen.configure(bg=self.__BACKGROUD_COLOR)

        # canvas do wyboru botow
        self.bot_choose_canvas = tk.Canvas(self.screen, width=300, height=200, bg=self.__BACKGROUD_COLOR,
                                           highlightthickness=0)
        self.bot_choose_canvas.pack(side="top", anchor="center", pady=50)

        def changeTagsBot1(screen):
            if self.bot1.get() == self.__ZAIMPLEMENTOWANE_BOTY[0] or self.bot1 == self.__ZAIMPLEMENTOWANE_BOTY[1]:
                label_bot_1_tag.config(text="   Głębkość ")

            if self.bot1.get() == self.__ZAIMPLEMENTOWANE_BOTY[2]:
                label_bot_1_tag.config(text="   Ilość iteracji: ")

        # Wybor bota 1
        label1 = tk.Label(self.bot_choose_canvas, text="BOT 1: ", font=("Arial", 12), bg=self.__BACKGROUD_COLOR)
        label1.grid(row=0, column=0)
        bot_menu1 = tk.OptionMenu(self.bot_choose_canvas, self.bot1, *self.__ZAIMPLEMENTOWANE_BOTY,
                                  command=changeTagsBot1)
        bot_menu1.grid(row=0, column=1)
        label_bot_1_tag = tk.Label(self.bot_choose_canvas, text="   Głębkość ", font=("Arial", 12),
                                   bg=self.__BACKGROUD_COLOR)
        label_bot_1_tag.grid(row=0, column=2)
        self.bot1_value = tk.Entry(self.bot_choose_canvas)
        self.bot1_value.grid(row=0, column=3)

        start_button = tk.Button(self.screen, text="Rozpocznij gre", fg="black",
                                 command=lambda: self.gra1v1(self.bot1_value.get()),
                                 height=self.__WYSOKOSC_PRZYCISKU, width=self.__SZEROKOSC_PRZYCISKU_MENU,
                                 bg=self.__BUTTONS_COLOR)
        start_button.place(x=self.__ODLEGLOSC_OD_PRAWEJ_KRAWEDZI_PRZYCISKU_MENU, y=225)

        return_button = tk.Button(self.screen, text="Powrót", fg="black", command=lambda: self.mainMenu(),
                                  height=self.__WYSOKOSC_PRZYCISKU, width=self.__SZEROKOSC_PRZYCISKU_MENU,
                                  bg=self.__BUTTONS_COLOR)
        return_button.place(x=self.__ODLEGLOSC_OD_PRAWEJ_KRAWEDZI_PRZYCISKU_MENU, y=400)

    def gra1v1(self, v1):
        if self.bot1.get() == "MinMax":
            # TODO Dodac opcje wyboru glebi dzialania minmaxa, teraz jest hardcoded na 4
            self.instancjaBota1 = MinMaxAgent(2, v1)
        elif self.bot1.get() == "AlphaBeta":
            # TODO tak jak wyzej, dodac opcje wyboru glebi
            self.instancjaBota1 = MinMaxABAgent(2, v1)
        elif self.bot1.get() == "MonteCarloTreeSearch":
            # TODO tj wyżej ale ilosc iteracji i constant(?)
            self.instancjaBota1 = MonteCarloTreeSearchAgent(2, v1, 0.95)
        # MIEJSCE NA INNE BOTY, TRZEBA JE BEDZIE ZAINICJALIZOWAC WZGLEDEM WYBORU UZYTKOWNIKA Z DROP DOWN MENU
        board = Board()
        self.clear_window()
        while board.ifLast():
            self.clear_window()
            self.printBoard()
            break
