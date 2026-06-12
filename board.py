import random

import wlasnosci

RED    = "\033[31m"
GREEN  = "\033[32m"
BLUE   = "\033[34m"
YELLOW = "\033[33m"
ORANGE = "\033[38;5;208m"
PINK   = "\033[95m"
RESET  = "\033[0m"

ASK  = f"{BLUE}[ASK]{RESET} "
CONF = f"{GREEN}[CNF]{RESET} "
WARN = f"{YELLOW}[WRN]{RESET} "
ERR  = f"{RED}[ERR]{RESET} "
CFM  = f"{ORANGE}[CFM]{RESET} "

def pytanie_t_n():
    while True:
        odp = input(f"{ASK}t/n: ").strip().lower()

        if odp == "t":
            return True
        elif odp == "n":
            return False

        print(f"{ERR}Podaj tylko 't' albo 'n'")

class Plansza:
    def __init__(self):
        self.pola = self._utworz_liste_pol()
        self.wlasciciele = [None] * len(self.pola)


    def _utworz_liste_pol(self):
        return [
            ("Start", 0, 0),
            ("Karta graficzna #1", 1, 200),
            ("Karta graficzna #2", 1, 200),
            ("Procersor #1", 2, 150),
            ("Szansa", 777,0),
            ("Procersor #2", 2, 150),
            ("Dysk twardy #1", 3, 50),
            ("Dysk twardy #2", 3, 50),
            ("Neostrada", 999,0),
            ("Pamięć RAM #1",4, 300),
            ("Pamięć RAM #2", 4, 300),
            ("Karta sieciowa #1", 5, 75),
            ("Ryzyko", 666,0),
            ("Karta sieciowa #2", 5, 75),
            ("Serwis komputerowy #1", 6, 25),
            ("Serwis komputerowy #2", 6, 25),

        ]

    def wypisanie_pola(self,numer_pola):

        pola = [
            "Start",
            "Karta graficzna #1",
            "Karta graficzna #2",
            "Procersor #1",
            "Szansa",
            "Procersor #2",
            "Dysk twardy #1",
            "Dysk twardy #2",
            "Neostrada",
            "Pamięć RAM #1",
            "Pamięć RAM #2",
            "Karta sieciowa #1",
            "Ryzyko",
            "Karta sieciowa #2",
            "Serwis komputerowy #1",
            "Serwis komputerowy #2"]
        return pola[numer_pola]

    def czy_do_kupienia(self, numer_pola, pieniadze,posiadane_pola_x, posiadane_pola_y, lista_pol):
        cena_pola = lista_pol[numer_pola][2]
        niekupowalne_pola = [0, 4, 8, 12]

        if numer_pola in niekupowalne_pola:
            return False, cena_pola

        if numer_pola in posiadane_pola_x or numer_pola in posiadane_pola_y:
            return False, cena_pola

        if pieniadze < cena_pola:
            return False, cena_pola

        print(f"{ASK}Czy chcesz kupić pole?")
        decyzja = pytanie_t_n()

        if decyzja:
            return True, cena_pola

        return False, cena_pola

    def czy_do_zaplaty(self, numer_pola, posiadane_pola_przeciwnika,pieniadze, lista_pol):
        typ = lista_pol[numer_pola][1]
        licznik = 0
        for pole in posiadane_pola_przeciwnika:
            if lista_pol[pole][1] == typ:
                licznik += 1
        if licznik >= 2:
            cena_pola = round(lista_pol[numer_pola][2] * 0.75)
        else:
            cena_pola = round(lista_pol[numer_pola][2] * 0.50)
        if numer_pola in posiadane_pola_przeciwnika:
            return True, cena_pola, pieniadze >= cena_pola

        return False, cena_pola, False

    def czy_szansa(self, numer_pola, pieniadze, posiadane_pola_gracza):

        if numer_pola != 4:
            return 0
        if not hasattr(self, "szanse"):
            self.szanse = [1, 2, 3]
        if not self.szanse:
            self.szanse = [1, 2, 3]
        element = random.choice(self.szanse)
        self.szanse.remove(element)
        if element == 1:
            print(f"{CFM}Brawo wygrałeś 100 dolarków")
            return 1
        if element == 2:
            print(f"{CFM}Brawo wygrałeś 2 dodatkowe ruchy")
            return 2

        if element == 3:
            print(f"{CFM}Brawo przechodzisz na start i odbierasz 200 dolarków za przejście")
            return 3

    def czy_ryzyko(self, numer_pola, pieniadze, posiadane_pola_gracza):
        if numer_pola != 12:
            return 0
        if not hasattr(self, "ryzyko"):
            self.ryzyko = [1, 2, 3,4]
        if not self.ryzyko:
            self.ryzyko = [1, 2, 3,4]
        element = random.choice(self.ryzyko)
        self.ryzyko.remove(element)
        if element == 1:
            print(f"{CFM}Brawo wygrałeś 200 dolarków")
            return 1
        if element == 2:
            print(f"{CFM}Słabo straciłeś 300 dolarków")
            return 2
        if element == 3:
            print(f"{CFM}Cofasz się na start ale nie odbierasz 200 dolarków za przejście")
            return 3
        if element == 4:
            print(f"{CFM}Tracisz ture :(")

    def czy_neostrada(self,numer_pola):
        if numer_pola != 8:
            return 0
        else:
            print(f"{CFM}Gdzie się chcesz przenieść?")
            return 1
    def czy_start(self,pozycja_gracza_x,wczesniejsza_pozycja_gracza_x):
        if pozycja_gracza_x >= 0 and wczesniejsza_pozycja_gracza_x > 0:
            print(f"{CFM}Otrzymujesz 200 dolarków za przejście przez start")
            return True
        else:
            return False

    def czy_wygral(self, posiadane_pola_gracza,gracz):

        typy_gracza = set()

        for pole in posiadane_pola_gracza:
            typ = self.pola[pole][1]
            typy_gracza.add(typ)

        wymagane_typy = {1, 2, 3, 4, 5, 6}

        if wymagane_typy.issubset(typy_gracza):
            print(f"{PINK}Gracz:{gracz} zebrał wszystkie komponenty!")
            return True

        return False

    def rysuj_plansze(self,pozycja_gracza_x, pozycja_gracza_y, posiadane_gracza_x, posiadane_gracza_y):
        gracz = f"{YELLOW}x {RESET}"
        lista_pol = ["  ","  ","  ","  ","  ","  ","  ","  ","  ","  ","  ","  ","  ","  ","  ","  ",]
        if pozycja_gracza_x == pozycja_gracza_y:
            lista_pol[pozycja_gracza_y] = f"{ORANGE}x{BLUE}y{RESET}"
        else:
            lista_pol[pozycja_gracza_x] = f"{YELLOW}x{RESET} "
            lista_pol[pozycja_gracza_y] = f"{BLUE}y{RESET} "


        posiadane_pola = [" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," ",]
        if posiadane_gracza_x:
            for pole in posiadane_gracza_x:
                posiadane_pola[pole] = f"{ORANGE}x{RESET}"

        if posiadane_gracza_y:
            for pole in posiadane_gracza_y:
                posiadane_pola[pole] = f"{BLUE}y{RESET}"
        plansza = [
            "==========================================================================================================",
            "|                    |                    |                    |                    |                    |",
            f"|{lista_pol[0]}                  |{lista_pol[1]}                  |{lista_pol[2]}                  |{lista_pol[3]}                  |{lista_pol[4]}                  |",
            "|Start               |Karta graficzna #1  |Karta graficzna #2  |Procesor #1         |Szansa              |",
            "|Dobierz 100         |200                 |200                 |150                 |                    |",
            f"|Posiadane przez:{posiadane_pola[0]}   |Posiadane przez:{posiadane_pola[1]}   |Posiadane przez:{posiadane_pola[2]}   |Posiadane przez:{posiadane_pola[3]}   |Posiadane przez:{posiadane_pola[4]}   |",
            "==========================================================================================================",
            "|                    |                                                              |                    |",
            f"|{lista_pol[15]}                  |                                                              |{lista_pol[5]}                  |",
            "|Serwis komputerow #2|                                                              |Procersor #2        |",
            "|25                  |                                                              |150                 |",
            f"|Posiadane przez:{posiadane_pola[15]}   |                                                              |Posiadane przez:{posiadane_pola[5]}   |",
            "======================                                                              ======================",
            "|                    |                                                              |                    |",
            f"|{lista_pol[14]}                  |                                                              |{lista_pol[6]}                  |",
            "|Serwis komputerow #1|                                                              |Dysk twardy#1       |",
            "|25                  |                                                              |50                  |",
            f"|Posiadane przez:{posiadane_pola[14]}   |                                                              |Posiadane przez:{posiadane_pola[6]}   |",
            "======================                                                              ======================",
            "|                    |                                                              |                    |",
            f"|{lista_pol[13]}                  |                                                              |{lista_pol[7]}                  |",
            "|Karta sieciowa #2   |                                                              |Dysk twardy#2       ",
            "|75                  |                                                              |50                  |",
            f"|Posiadane przez:{posiadane_pola[13]}   |                                                              |Posiadane przez:{posiadane_pola[7]}   |",
            "==========================================================================================================",
            "|                    |                    |                    |                    |                    |",
            f"|{lista_pol[12]}                  |{lista_pol[11]}                  |{lista_pol[10]}                  |{lista_pol[9]}                  |{lista_pol[8]}                  |",
            "|Ryzyko              |Karta sieciowa #1   |Pamięć RAM #2       |Pamięć RAM #1       |Neostrada           |",
            "|                    |75                  |300                 |300                 |                    |",
            f"|Posiadane przez:{posiadane_pola[12]}   |Posiadane przez:{posiadane_pola[11]}   |Posiadane przez:{posiadane_pola[10]}   |Posiadane przez:{posiadane_pola[9]}   |Posiadane przez:{posiadane_pola[8]}   |",
            "==========================================================================================================",
        ]

        for linia in plansza:
            print(linia)