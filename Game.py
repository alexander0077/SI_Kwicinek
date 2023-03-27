class Game:
    __szerokosc = 0
    __wysokosc = 0
    # gameArr ma wartosci 0 - nic nie ma, 1- gracz jeden ma krazek, 2- gracz 2 ma krazek na danym miejscu
    __gameArr = None
    current_Player = 1

    def __init__(self, szerokosc=7, wysokosc=6):
        self.__wysokosc = wysokosc
        self.__szerokosc = szerokosc
        self.__gameArr = [([0] * szerokosc) for _ in range(wysokosc)]

    def dodajKrazek(self, x):
        for i in range(self.__wysokosc-1, -1, -1):
            # petla leci od tylu z powodu indeksowania
            # [0,0] [0,1] [0,2] [0,3] ... [0, szerokosc]
            # [1,0] [1,1] [1,2] [1,3] ... [1, szerokosc]
            # [2,0] [2,1] [2,2] [2,3] ... [2, szerokosc]
            # [3,0] [3,1] [3,2] [3,3] ... [3, szerokosc]
            # [4,0] [4,1] [4,2] [4,3] ... [4, szerokosc]
            # [5,0] [5,1] [5,2] [5,3] ... [5, szerokosc]
            # [6,0] [6,1] [6,2] [6,3] ... [6, szerokosc]
            # ...   ...   ...   ...  ...  ...
            # [wysokosc,0] [wysokosc,1] [wysokosc,2] [wysokosc,3] ... [wysoksc, szerokosc]
            if self.__gameArr[i][x] == 0:
                self.__gameArr[i][x] = self.current_Player
                # wykonano legalny ruch, spr czy wygrana, jesli tak zwroc jakis numer, jesli nie to zwroc 0

                if self.sprawdzWygrana(self.current_Player):
                    return 10 + self.current_Player
                if self.current_Player == 1:
                    self.current_Player = 2
                else:
                    self.current_Player = 1
                return 0
        # nie mozna wykonac ruchu, bo sie plansza przepelni, zwroc 1
        return 1

    def sprawdzWygrana(self, gracz):
        # check horizontal loc
        for c in range(self.__szerokosc - 3):
            for r in range(self.__wysokosc):
                if self.__gameArr[r][c] == gracz and self.__gameArr[r][c + 1] == gracz and \
                        self.__gameArr[r][c + 2] == gracz and self.__gameArr[r][c + 3] == gracz:
                    return True

            # Check vertical locations for win
        for c in range(self.__szerokosc):
            for r in range(self.__wysokosc - 3):
                if self.__gameArr[r][c] == gracz and self.__gameArr[r + 1][c] == gracz and \
                        self.__gameArr[r + 2][c] == gracz and self.__gameArr[r + 3][c] == gracz:
                    return True

            # Check positively sloped diagonals
        for c in range(self.__szerokosc - 3):
            for r in range(self.__wysokosc - 3):
                if self.__gameArr[r][c] == gracz and self.__gameArr[r + 1][c + 1] == gracz and \
                        self.__gameArr[r + 2][c + 2] == gracz and self.__gameArr[r + 3][c + 3] == gracz:
                    return True

            # Check negatively sloped diaganols
        for c in range(self.__szerokosc - 3):
            for r in range(3, self.__wysokosc):
                if self.__gameArr[r][c] == gracz and self.__gameArr[r - 1][c + 1] == gracz and \
                        self.__gameArr[r - 2][c + 2] == gracz and self.__gameArr[r - 3][c + 3] == gracz:
                    return True

    def getArr(self):
        return self.__gameArr
