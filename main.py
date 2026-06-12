import random
import os
import sys

import board
import wlasnosci


plansza = board.Plansza()
wlasnosci.plansza = plansza


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
        odp = input("t/n: ").strip().lower()

        if odp in ("t", "n"):
            return odp

        print("Podaj tylko 't' albo 'n'")

def clear_terminal():
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
    except:
        print("\033[2J\033[H", end="")




def intro():
    print(f"{CONF}Tymczasowe")
    wlasnosci.pieniadze_x = 1000
    wlasnosci.pieniadze_y = 1000
    print(f"{CONF}Każdy z graczy na start otrzymuje 1000 dolarków")
    wlasnosci.czy_tura_x = 1

def kostka():
    print(f"{ASK}Naciśnij ENTER aby wylosować")
    input()
    wylosowane = random.randint(1, 6)
    clear_terminal()
    print(f"{CONF}Wylosowane:{RED}{wylosowane}{RESET}")

    return wylosowane
def czy_przegral(pieniadze,gracz):
    if gracz == "x":
        przeciwnik = "y"
    else: przeciwnik = "x"
    if pieniadze < 0:
        print(f"{WARN}Przegrano graczu {gracz}, wygrał gracz {przeciwnik}")
        return True
    return False


def tura_dla_x():
    clear_terminal()
    wlasnosci.wyswietlenie_info(wlasnosci.pieniadze_x, wlasnosci.posiadane_pola_x, wlasnosci.czy_tura_x)
    plansza.rysuj_plansze(
        wlasnosci.pozycja_gracza_x,
        wlasnosci.pozycja_gracza_y,
        wlasnosci.posiadane_pola_x,
        wlasnosci.posiadane_pola_y
    )
    print("\n")
    wczesniejsza_pozycja_gracza = wlasnosci.pozycja_gracza_x
    wlasnosci.pozycja_gracza_x = wlasnosci.pozycja_gracza_x + kostka()
    if wlasnosci.pozycja_gracza_x >= 16:
        wlasnosci.pozycja_gracza_x %= 16
    plansza.rysuj_plansze(
        wlasnosci.pozycja_gracza_x,
        wlasnosci.pozycja_gracza_y,
        wlasnosci.posiadane_pola_x,
        wlasnosci.posiadane_pola_y
    )
    zakup_ok, cena = plansza.czy_do_kupienia(wlasnosci.pozycja_gracza_x,wlasnosci.pieniadze_x, wlasnosci.posiadane_pola_x, wlasnosci.posiadane_pola_y,plansza._utworz_liste_pol())
    zaplata_ok, cena, ma_pieniadze = plansza.czy_do_zaplaty(wlasnosci.pozycja_gracza_x,wlasnosci.posiadane_pola_y,wlasnosci.pieniadze_x, plansza._utworz_liste_pol())
    if zakup_ok == True:
        wlasnosci.pieniadze_x = wlasnosci.pieniadze_x - cena
        print(f"{CONF}Zakupiono pole:{plansza.wypisanie_pola(wlasnosci.pozycja_gracza_x)}")
        wlasnosci.posiadane_pola_x.append(wlasnosci.pozycja_gracza_x)
    elif zaplata_ok == True:
        wlasnosci.pieniadze_x = wlasnosci.pieniadze_x - cena
        wlasnosci.pieniadze_y = wlasnosci.pieniadze_y + cena
        print(f"{CONF}Zapłacano za wejście na pole:{cena}")
    szansa = plansza.czy_szansa(wlasnosci.pozycja_gracza_x,wlasnosci.pieniadze_x,wlasnosci.posiadane_pola_x)
    if szansa != 0:
        if szansa == 1:
            wlasnosci.pieniadze_x = wlasnosci.pieniadze_x + 100
        if szansa == 2:
            wlasnosci.czy_tura_x = wlasnosci.czy_tura_x + 2
        if szansa == 3:
            wlasnosci.pieniadze_x = wlasnosci.pieniadze_y + 200
            wlasnosci.pozycja_gracza_x = 0
    ryzyko = plansza.czy_ryzyko(wlasnosci.pozycja_gracza_x, wlasnosci.pieniadze_x, wlasnosci.posiadane_pola_x)
    if ryzyko != 0:
        if ryzyko == 1:
            wlasnosci.pieniadze_x = wlasnosci.pieniadze_x + 200
        if ryzyko == 2:
            wlasnosci.pieniadze_x = wlasnosci.pieniadze_x - 300
        if ryzyko == 3:
            wlasnosci.pozycja_gracza_x = 0
        if ryzyko == 4:
            wlasnosci.czy_tura_x = wlasnosci.czy_tura_x - 1
    neostrada = plansza.czy_neostrada(wlasnosci.pozycja_gracza_x)
    if neostrada == 1:
        pole = int(input(f"{ASK}Numer pola: "))
        wlasnosci.pozycja_gracza_x = pole
    start = plansza.czy_start(wlasnosci.pozycja_gracza_x,wczesniejsza_pozycja_gracza)
    if start:
        wlasnosci.pieniadze_x = wlasnosci.pieniadze_x + 200


    wlasnosci.wyswietlenie_info(wlasnosci.pieniadze_x, wlasnosci.posiadane_pola_x, wlasnosci.czy_tura_x)
    wlasnosci.czy_tura_x = wlasnosci.czy_tura_x - 1
    if wlasnosci.czy_tura_x <= 0:
        wlasnosci.czy_tura_y = wlasnosci.czy_tura_y + 1

def tura_dla_y():
    clear_terminal()

    wlasnosci.wyswietlenie_info(
        wlasnosci.pieniadze_y,
        wlasnosci.posiadane_pola_y,
        wlasnosci.czy_tura_y
    )

    plansza.rysuj_plansze(
        wlasnosci.pozycja_gracza_y,
        wlasnosci.pozycja_gracza_x,
        wlasnosci.posiadane_pola_y,
        wlasnosci.posiadane_pola_x
    )

    print("\n")

    wczesniejsza_pozycja_gracza = wlasnosci.pozycja_gracza_y
    wlasnosci.pozycja_gracza_y += kostka()
    if wlasnosci.pozycja_gracza_x >= 16:
        wlasnosci.pozycja_gracza_x %= 16
    plansza.rysuj_plansze(
        wlasnosci.pozycja_gracza_y,
        wlasnosci.pozycja_gracza_x,
        wlasnosci.posiadane_pola_y,
        wlasnosci.posiadane_pola_x
    )

    zakup_ok, cena = plansza.czy_do_kupienia(
        wlasnosci.pozycja_gracza_y,
        wlasnosci.pieniadze_y,
        wlasnosci.posiadane_pola_y,
        wlasnosci.posiadane_pola_x,
        plansza._utworz_liste_pol()
    )

    zaplata_ok, cena, ma_pieniadze = plansza.czy_do_zaplaty(
        wlasnosci.pozycja_gracza_y,
        wlasnosci.posiadane_pola_x,
        wlasnosci.pieniadze_y,
        plansza._utworz_liste_pol()
    )

    if zakup_ok:
        wlasnosci.pieniadze_y -= cena
        print(f"{CONF}Zakupiono pole:{plansza.wypisanie_pola(wlasnosci.pozycja_gracza_y)}")
        wlasnosci.posiadane_pola_y.append(wlasnosci.pozycja_gracza_y)

    elif zaplata_ok:
        wlasnosci.pieniadze_y -= cena
        wlasnosci.pieniadze_x += cena
        print(f"{CONF}Zapłacano za wejście na pole:{cena}")

    szansa = plansza.czy_szansa(
        wlasnosci.pozycja_gracza_y,
        wlasnosci.pieniadze_y,
        wlasnosci.posiadane_pola_y
    )

    if szansa == 1:
        wlasnosci.pieniadze_y += 100

    elif szansa == 2:
        wlasnosci.czy_tura_y += 2

    elif szansa == 3:
        wlasnosci.pieniadze_y += 200
        wlasnosci.pozycja_gracza_y = 0

    ryzyko = plansza.czy_ryzyko(
        wlasnosci.pozycja_gracza_y,
        wlasnosci.pieniadze_y,
        wlasnosci.posiadane_pola_y
    )

    if ryzyko == 1:
        wlasnosci.pieniadze_y += 200

    elif ryzyko == 2:
        wlasnosci.pieniadze_y -= 300

    elif ryzyko == 3:
        wlasnosci.pozycja_gracza_y = 0

    elif ryzyko == 4:
        wlasnosci.czy_tura_y -= 1

    neostrada = plansza.czy_neostrada(wlasnosci.pozycja_gracza_y)

    if neostrada == 1:
        pole = int(input(f"{ASK}Numer pola: "))
        wlasnosci.pozycja_gracza_x = pole - 1

    start = plansza.czy_start(
        wlasnosci.pozycja_gracza_y,
        wczesniejsza_pozycja_gracza
    )

    if start:
        wlasnosci.pieniadze_y += 200

    wlasnosci.wyswietlenie_info(
        wlasnosci.pieniadze_y,
        wlasnosci.posiadane_pola_y,
        wlasnosci.czy_tura_y
    )

    wlasnosci.czy_tura_y -= 1

    if wlasnosci.czy_tura_y <= 0:
        wlasnosci.czy_tura_x += 1

def main():
    intro()

    while True:

        if wlasnosci.czy_tura_x > 0:
            tura_dla_x()

            przegrana = czy_przegral(wlasnosci.pieniadze_x, "x")
            if przegrana:
                clear_terminal()
                wlasnosci.wyswietlenie_info(
                    wlasnosci.pieniadze_x,
                    wlasnosci.posiadane_pola_x,
                    wlasnosci.czy_tura_x
                )
                break

            if plansza.czy_wygral(wlasnosci.posiadane_pola_x,"x"):
                print("X wygrał!")
                break

        if wlasnosci.czy_tura_y > 0:
            tura_dla_y()

            przegrana = czy_przegral(wlasnosci.pieniadze_y, "y")
            if przegrana:
                clear_terminal()
                wlasnosci.wyswietlenie_info(
                    wlasnosci.pieniadze_y,
                    wlasnosci.posiadane_pola_y,
                    wlasnosci.czy_tura_y
                )
                break

            if plansza.czy_wygral(wlasnosci.posiadane_pola_y,"y"):
                print("Y wygrał!")
                break




if __name__ == "__main__":
    main()