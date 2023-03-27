from tkinter import Tk
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


    def mainMenu(self, screen):
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

    def graBOT(self, screen):

        print("botek")

    def gra1v1(self, screen):
        print("niebotek")