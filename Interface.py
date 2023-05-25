import time
from tkinter import Tk
from tkinter import ttk

from Agenty.Train import GameLoop
from Agenty.alphabetaagent import MinMaxABAgent
from Agenty.montecarloagent import MonteCarloTreeSearchAgent
from Agenty.regresjaagent import RegresjaAgent
from Agenty.randomagent import RandomAgent
from Agenty.heuristicagent import StaticAgent
from Agenty.networkagent import NetworkAgent
from Board import Board
import tkinter as tk
from Game import Game
from Agenty.minmaxagent import MinMaxAgent


class Interface:
    __ZAIMPLEMENTOWANE_BOTY = [
        "MinMax",
        "AlphaBeta",
        "MonteCarloTreeSearch",
        "Random",
        "Heurystyka statyczna",
        "Siec neuronowa"
    ]
    __SZEROKOSC_EKRANU = 900
    __WYSOKOSC_EKRANU = 600
    __SZEROKOSC_PRZYCISKU_MENU = 40
    __ODLEGLOSC_OD_PRAWEJ_KRAWEDZI_PRZYCISKU_MENU = 310
    __BACKGROUD_COLOR = '#adad9a'
    __BUTTONS_COLOR = '#d1c75a'
    __WYSOKOSC_PRZYCISKU = 4

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
        self.potrzebny_trening = True
        self.turn = tk.StringVar(self.screen)
        self.enemy_stat = 3

        self.sumaCzasu1 = 0
        self.sumaCzasu2 = 0
        self.sumaRuchow1 = 0.0001
        self.sumaRuchow2 = 0.0001

        self.mainMenu()



    def mainMenu(self):  # GLOWNY INTERFACE Z WYBOREM TRYBU I WYJSCIEM
        self.game.reset()
        self.sumaCzasu1 = 0
        self.sumaCzasu2 = 0
        self.sumaRuchow1 = 0.0001
        self.sumaRuchow2 = 0.0001
        self.instancjaBota2 = None
        self.instancjaBota1 = None
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
        if self.instancjaBota1 is None:
            name = "Gracz 1"
        else:
            name = self.instancjaBota1.toString()
        player_1_canvas.create_text((self.__SZEROKOSC_EKRANU - canvas_width) / 4, 150,
                                    text=name + "\n",
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
        # ===================================TIMER=============================================
        if self.instancjaBota1 is not None:
            player_1_canvas.create_text((self.__SZEROKOSC_EKRANU - canvas_width) / 4, 305,
                                        text="Średni czas ruchu:",
                                        font=("Arial", 17))

            player_1_canvas.create_text((self.__SZEROKOSC_EKRANU - canvas_width) / 4, 355,
                                        text=str(round((self.sumaCzasu1 / self.sumaRuchow1) * 100)/100) + "ms",
                                        font=("Arial", 25))
        # ===================================TIMER=============================================

        canvas = tk.Canvas(self.screen, width=canvas_width, height=canvas_height, highlightthickness=0)
        canvas.configure(bg=self.__BACKGROUD_COLOR)
        canvas.pack(side="left")

        player_2_canvas = tk.Canvas(self.screen, width=(self.__SZEROKOSC_EKRANU - canvas_width) / 2,
                                    height=canvas_height, highlightthickness=0)
        player_2_canvas.configure(bg=self.__BACKGROUD_COLOR)
        player_2_canvas.pack(side="left", padx=0, pady=0)

        player_2_canvas.create_text((self.__SZEROKOSC_EKRANU - canvas_width) / 4, 70, text='PLAYER 2:',
                                    font=("Arial", 16))

        if self.instancjaBota2 is None:
            name_2 = "Gracz 2"
        else:
            name_2 = self.instancjaBota2.toString()

        player_2_canvas.create_text((self.__SZEROKOSC_EKRANU - canvas_width) / 4, 150,
                                    text=name_2 + "\n",
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
#===================================TIMER=============================================
        if self.instancjaBota2 is not None:
            player_2_canvas.create_text((self.__SZEROKOSC_EKRANU - canvas_width) / 4, 305,
                                        text="Średni czas ruchu:",
                                        font=("Arial", 17))

            player_2_canvas.create_text((self.__SZEROKOSC_EKRANU - canvas_width) / 4, 355,
                                        text=str(round((self.sumaCzasu2 / self.sumaRuchow2) * 100)/100) + "ms",
                                        font=("Arial", 25))
# ===================================TIMER=============================================

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

        if self.instancjaBota2 is None or self.instancjaBota1 is None:
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
        elif self.bot1.get() == "Random":
            self.instancjaBota1 = RandomAgent(1)
        elif self.bot1.get() == "MonteCarloTreeSearch":
            self.instancjaBota1 = MonteCarloTreeSearchAgent(1, int(v1), 0.95)
        elif self.bot1.get() == "Heurystyka statyczna":
            self.instancjaBota1 = StaticAgent(1)
        elif self.bot1.get() == "Siec neuronowa":
            self.instancjaBota1 = NetworkAgent(1)


        if self.bot2.get() == "MinMax":
            self.instancjaBota2 = MinMaxAgent(2, int(v2))
        elif self.bot2.get() == "AlphaBeta":
            self.instancjaBota2 = MinMaxABAgent(2, int(v2))
        elif self.bot2.get() == "Random":
            self.instancjaBota2 = RandomAgent(2)
        elif self.bot2.get() == "MonteCarloTreeSearch":
            self.instancjaBota2 = MonteCarloTreeSearchAgent(2, int(v2), 0.95)
        elif self.bot2.get() == "Heurystyka statyczna":
            self.instancjaBota2 = StaticAgent(2)
        elif self.bot2.get() == "Siec neuronowa":
            self.instancjaBota2 = NetworkAgent(2)

        self.clear_window()
        if not self.boardNotFull():
            self.last_winner = "Remis"
        while self.game.wining_player == -1 and self.boardNotFull():
            self.clear_window()
            self.printBoard()

            t1 = time.time()
            self.game.dodajKrazek(self.instancjaBota1.decide(self.game))
            t2 = time.time()
            self.sumaCzasu1 += round((t2 - t1) * 100000)/100
            self.sumaRuchow1 += 1

            self.clear_window()
            self.printBoard()
            self.screen.update_idletasks()
            self.screen.update()

            t1 = time.time()
            self.game.dodajKrazek(self.instancjaBota2.decide(self.game))
            t2 = time.time()
            self.sumaCzasu2 += round((t2 - t1) * 100000)/100
            self.sumaRuchow2 += 1

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
            if self.bot1.get() == self.__ZAIMPLEMENTOWANE_BOTY[0] or self.bot1.get() == self.__ZAIMPLEMENTOWANE_BOTY[1]:
                label_bot_1_tag.config(text="   Głębkość ")
                self.bot1_value.grid(row=0, column=3)
            elif self.bot1.get() == self.__ZAIMPLEMENTOWANE_BOTY[2]:
                label_bot_1_tag.config(text="   Ilość iteracji: ")
                self.bot1_value.grid(row=0, column=3)
            else:
                label_bot_1_tag.config(text="                   ")
                self.bot1_value.grid_remove()

        def changeTagsBot2(screen):
            if self.bot2.get() == self.__ZAIMPLEMENTOWANE_BOTY[0] or self.bot2.get() == self.__ZAIMPLEMENTOWANE_BOTY[1]:
                label_bot_2_tag.config(text="   Głębkość ")
                self.bot2_value.grid(row=1, column=3)
            elif self.bot2.get() == self.__ZAIMPLEMENTOWANE_BOTY[2]:
                label_bot_2_tag.config(text="   Ilość iteracji: ")
                self.bot2_value.grid(row=1, column=3)
            else:
                label_bot_2_tag.config(text="                   ")
                self.bot2_value.grid_remove()

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


    def winnerFoundInGameVBot(self):
        if self.game.wining_player == 1:
            self.wygraneBot1 += 1
            if self.instancjaBota1 is not None:
                name = self.instancjaBota1.toString()
            else:
                name = "Gracz 1"
            self.last_winner = "Wygrywa: " + name
            self.lastWinTime = time.time()
        elif self.game.wining_player == 2:
            if self.instancjaBota2 is not None:
                name = self.instancjaBota2.toString()
            else:
                name = "Gracz 2"

            self.last_winner = "Wygrywa: " + name
            self.wygraneBot2 += 1
            self.lastWinTime = time.time()
        elif self.game.wining_player == 0:
            self.wygraneBot1 += 0.5
            self.wygraneBot2 += 0.5
            self.lastWinTime = time.time()

    def move(self, i):
        #if self.game.current_Player == 2:
        #    return
        self.game.dodajKrazek(i)
        if self.game.wining_player != -1:
            self.winnerFoundInGameVBot()
            self.game.reset()
            self.gra1v1()
            return

        self.clear_window()
        self.printBoard()
        if self.instancjaBota1 is not None:
            t1 = time.time()
            self.game.dodajKrazek(self.instancjaBota1.decide(self.game))
            t2 = time.time()
            self.sumaCzasu1 += round((t2 - t1) * 100000) / 100
            self.sumaRuchow1 += 1
        else:
            t1 = time.time()
            self.game.dodajKrazek(self.instancjaBota2.decide(self.game))
            t2 = time.time()
            self.sumaCzasu2 += round((t2 - t1) * 100000) / 100
            self.sumaRuchow2 += 1

        if self.game.wining_player != -1:
            self.winnerFoundInGameVBot()
            self.game.reset()
            self.gra1v1()
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
            if self.bot1.get() == self.__ZAIMPLEMENTOWANE_BOTY[0] or self.bot1.get() == self.__ZAIMPLEMENTOWANE_BOTY[1]:
                label_bot_1_tag.config(text="   Głębkość ")
                self.enemy_stat_entry.grid(row=0, column=3)
            elif self.bot1.get() == self.__ZAIMPLEMENTOWANE_BOTY[2]:
                label_bot_1_tag.config(text="   Ilość iteracji: ")
                self.enemy_stat_entry.grid(row=0, column=3)
            else:
                label_bot_1_tag.config(text="                   ")
                self.enemy_stat_entry.grid_remove()

        # Wybor bota 1
        label1 = tk.Label(self.bot_choose_canvas, text="BOT 1: ", font=("Arial", 12), bg=self.__BACKGROUD_COLOR)
        label1.grid(row=0, column=0)
        bot_menu1 = tk.OptionMenu(self.bot_choose_canvas, self.bot1, *self.__ZAIMPLEMENTOWANE_BOTY,
                                  command=changeTagsBot1)
        bot_menu1.grid(row=0, column=1)
        label_bot_1_tag = tk.Label(self.bot_choose_canvas, text="   Głębkość ", font=("Arial", 12),
                                   bg=self.__BACKGROUD_COLOR)
        label_bot_1_tag.grid(row=0, column=2)
        self.enemy_stat_entry = tk.Entry(self.bot_choose_canvas)
        self.enemy_stat_entry.grid(row=0, column=3)

        label_choose_side = tk.Label(self.bot_choose_canvas, text="Wybierz strone: ", font=("Arial", 12), bg=self.__BACKGROUD_COLOR)
        label_choose_side.grid(row=1, column=0)

        options_on_who_start = ["Gracz 1", "Gracz 2"]
        choose_side_menu = tk.OptionMenu(self.bot_choose_canvas, self.turn, *options_on_who_start)
        choose_side_menu.grid(row=1, column=1)

        start_button = tk.Button(self.screen, text="Rozpocznij gre", fg="black",
                                 command=lambda: self.gra1v1(self.enemy_stat_entry.get()),
                                 height=self.__WYSOKOSC_PRZYCISKU, width=self.__SZEROKOSC_PRZYCISKU_MENU,
                                 bg=self.__BUTTONS_COLOR)
        start_button.place(x=self.__ODLEGLOSC_OD_PRAWEJ_KRAWEDZI_PRZYCISKU_MENU, y=225)

        return_button = tk.Button(self.screen, text="Powrót", fg="black", command=lambda: self.mainMenu(),
                                  height=self.__WYSOKOSC_PRZYCISKU, width=self.__SZEROKOSC_PRZYCISKU_MENU,
                                  bg=self.__BUTTONS_COLOR)
        return_button.place(x=self.__ODLEGLOSC_OD_PRAWEJ_KRAWEDZI_PRZYCISKU_MENU, y=400)

    def gra1v1(self, staty=None):
        self.game.reset()

        if staty == None: # tu jest makaron z typami, nie przejmujcie sie
            v1 = self.enemy_stat
        else:
            if staty != '':
                v1 = int(staty)
                self.enemy_stat = v1
            else:
                v1 = 0

        player = 2
        if self.turn.get() == "Gracz 2":
            player = 1
            if self.bot1.get() == "MinMax":
                self.instancjaBota1 = MinMaxAgent(player, v1)
            elif self.bot1.get() == "AlphaBeta":
                self.instancjaBota1 = MinMaxABAgent(player, v1)
            elif self.bot1.get() == "Random":
                self.instancjaBota1 = RandomAgent(player)
            elif self.bot1.get() == "MonteCarloTreeSearch":
                self.instancjaBota1 = MonteCarloTreeSearchAgent(player, v1, 0.95)
            elif self.bot1.get() == "Heurystyka statyczna":
                self.instancjaBota1 = StaticAgent(player)
            elif self.bot1.get() == "Siec neuronowa":
                self.instancjaBota1 = NetworkAgent(player)
        else:
            if self.bot1.get() == "MinMax": # nie wazne ze jest bot1 - jest git
                self.instancjaBota2 = MinMaxAgent(player, v1)
            elif self.bot1.get() == "AlphaBeta":
                self.instancjaBota2 = MinMaxABAgent(player, v1)
            elif self.bot1.get() == "Random":
                self.instancjaBota2 = RandomAgent(player)
            elif self.bot1.get() == "MonteCarloTreeSearch":
                self.instancjaBota2 = MonteCarloTreeSearchAgent(player, v1, 0.95)
            elif self.bot1.get() == "Heurystyka statyczna":
                self.instancjaBota2 = StaticAgent(player)
            elif self.bot1.get() == "Siec neuronowa":
                self.instancjaBota2 = NetworkAgent(player)



        # MIEJSCE NA INNE BOTY, TRZEBA JE BEDZIE ZAINICJALIZOWAC WZGLEDEM WYBORU UZYTKOWNIKA Z DROP DOWN MENU
        board = Board()
        self.clear_window()

        if player == 1:
            t1 = time.time()
            self.game.dodajKrazek(self.instancjaBota1.decide(self.game))
            t2 = time.time()
            self.sumaCzasu1 += round((t2 - t1) * 100000) / 100
            self.sumaRuchow1 += 1


        self.clear_window()
        self.printBoard()

