from tkinter import Tk
from Board import Board
import tkinter as tk

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

    def __init__(self):
        screen = Tk()
        screen.title('4 w linii')
        screen.geometry(str(self.__SZEROKOSC_EKRANU) + "x" + str(self.__WYSOKOSC_EKRANU))
        screen.resizable(False, False)
        self.mainMenu(screen)


    def mainMenu(self, screen):#GLOWNY INTERFACE Z WYBOREM TRYBU I WYJSCIEM
        for widgets in screen.winfo_children():
            widgets.destroy()
        screen.configure(bg=self.__BACKGROUD_COLOR)

        game_title = tk.Label(screen, text="4 IN LINE", font=('Arial', 32))
        game_title.place(relx=0.5, rely=0.04, anchor='n')
        game_title.configure(bg=self.__BACKGROUD_COLOR)
        game_title.configure(anchor='center')

        button_BOT = tk.Button(screen, text="Graj przeciwko SI", fg="black", command=lambda: self.graBOT(screen),
                                    height=self.__WYSOKOSC_PRZYCISKU, width=self.__SZEROKOSC_PRZYCISKU_MENU,
                               bg=self.__BUTTONS_COLOR)
        button_BOT.place(x=self.__ODLEGLOSC_OD_PRAWEJ_KRAWEDZI_PRZYCISKU_MENU, y=125)

        button_1v1 = tk.Button(screen, text="Gra na 2 graczy", fg="black", command=lambda: self.gra1v1(screen),
                               height=self.__WYSOKOSC_PRZYCISKU, width=self.__SZEROKOSC_PRZYCISKU_MENU,
                               bg=self.__BUTTONS_COLOR)
        button_1v1.place(x=self.__ODLEGLOSC_OD_PRAWEJ_KRAWEDZI_PRZYCISKU_MENU, y=225)

        button_wyjdz = tk.Button(screen, text="Wyjdź", fg="black", command=quit, height=self.__WYSOKOSC_PRZYCISKU,
                                    width=self.__SZEROKOSC_PRZYCISKU_MENU, bg=self.__BUTTONS_COLOR)
        button_wyjdz.place(x=self.__ODLEGLOSC_OD_PRAWEJ_KRAWEDZI_PRZYCISKU_MENU, y=375)

        screen.mainloop()

    def clear_window(self, screen):
        for widgets in screen.winfo_children():
            widgets.destroy()

    def printBoard(self, screen, board):
        board_rows = 6
        board_cols = 7
        canvas_width = 400
        canvas_height = 500
        cell_size = 40
        cell_padding = 5

        canvas = tk.Canvas(screen, width=canvas_width, height=canvas_height)
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
                if board.getCells()[board_rows - 1 - row][col] == 0:
                    canvas.create_rectangle(x1, y1, x2, y2, fill='white', outline='black')
                elif board.getCells()[board_rows - 1 - row][col] == 1:
                    canvas.create_rectangle(x1, y1, x2, y2, fill='blue', outline='black')
                else:
                    canvas.create_rectangle(x1, y1, x2, y2, fill='red', outline='black')

        for i in range(board_cols):
            button = tk.Button(screen, text="  ", command=lambda i=i: self.move(screen, i, board),
                               height=2, width=5)
            button.place(x=x1 - (cell_size + cell_padding)/2 + i * (cell_size + cell_padding), y= y2 + 20)

    def graBOT(self, screen): #TODO TU BEDZIE CALY PROJEKT TAK W SUMIE
        print("bot")

    def move(self, screen, i, board):
        board.addCoin(i)
        self.clear_window(screen)
        self.printBoard(screen, board)
    def gra1v1(self, screen):
        board = Board()
        self.clear_window(screen)
        while board.ifLast():
            self.clear_window(screen)
            self.printBoard(screen, board)
            break
