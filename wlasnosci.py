import board

pozycja_gracza_x = 0
posiadane_pola_x = [1]
pieniadze_x = 0
czy_tura_x = 0
czy_przegrana_x = 0

pozycja_gracza_y = 0
posiadane_pola_y = []
pieniadze_y = 0
czy_tura_y = 0
czy_przegrana_y = 0

plansza = None

def wyswietlenie_info(pieniadze, posiadane_pola, czy_tura):
    print("\n")
    print(f"Kasa: {pieniadze}")

    if posiadane_pola:
        for pole in posiadane_pola:
            print(f"Posiadane pole: {plansza.wypisanie_pola(pole)}")
    else:
        print("Brak posiadanych pól")
    print("\n")



