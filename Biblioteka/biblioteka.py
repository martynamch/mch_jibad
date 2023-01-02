# to nie jest zadanie na jeden plik

import csv
import os.path
import datetime
import calendar

dt = datetime.date.today()

month = dt.month
year = dt.year + month // 12
month = month % 12 + 1
day = min(dt.day, calendar.monthrange(year, month)[1])

def menu(options):
    options = list(options.items())
    print("Wybierz odpowiedni numer.")
    while True:
        for ind, option in enumerate(options, start=1):
            print("{}. {}".format(ind, option[0]))
        try:
            choice = int(input("Podaj numer: "))
            if 0 < choice <= len(options):
                func, args, kwargs = options[choice - 1][1]
                return func(*args, **kwargs)
        except ValueError:
            pass  # pusty except wymaga komentarza

def dodaj_ksiazke():  # ta funkcja łączy dialog z użytkownikiem i logikę biznesową

    tytul = input("Podaj tytuł: ")
    autor = input("Podaj autora: ")
    klucz = input("Podaj słowa kluczowe: ")

    if not os.path.isfile("katalog.csv"):
        with open("katalog.csv", "w", newline="") as catalog:
            headers = ["Tytul", "Autor", "Slowa kluczowe", "Wypozyczone przez", "Data zwrotu", "Zarezerwowane przez"]
            writer = csv.DictWriter(catalog, fieldnames=headers)
            writer.writeheader()
            writer.writerow({"Tytul": tytul,
                             "Autor": autor,
                             "Slowa kluczowe": klucz,
                             "Wypozyczone przez": "-",
                             "Data zwrotu": str(datetime.date(9999,1,1)),
                             "Zarezerwowane przez": "-"})
    else:  # DRY
        with open("katalog.csv", "a", newline="") as catalog:
            headers = ["Tytul", "Autor", "Slowa kluczowe", "Wypozyczone przez", "Data zwrotu", "Zarezerwowane przez"]
            writer = csv.DictWriter(catalog, fieldnames=headers)
            writer.writerow({"Tytul": tytul,
                             "Autor": autor,
                             "Slowa kluczowe": klucz,
                             "Wypozyczone przez": "-",
                             "Data zwrotu": str(datetime.date(9999,1,1)),
                             "Zarezerwowane przez": "-"})

    print("Ksiazka zostala dodana do katalogu.")

def usun_ksiazke():

    tytul = input("Podaj tytuł: ")
    autor = input("Podaj autora: ")

    with open("katalog.csv", "r", newline="") as catalog_in, open('katalog_new.csv', "w", newline="") as catalog_out:
        headers = ["Tytul", "Autor", "Slowa kluczowe", "Wypozyczone przez", "Data zwrotu", "Zarezerwowane przez"]
        writer = csv.DictWriter(catalog_out, fieldnames=headers)
        writer.writeheader()
        for row in csv.DictReader(catalog_in, delimiter=','):
            if row["Tytul"] != tytul and row["Autor"] != autor:
                writer.writerow({"Tytul": row["Tytul"],
                             "Autor": row["Autor"],
                             "Slowa kluczowe": row["Slowa kluczowe"],
                             "Wypozyczone przez": row["Wypozyczone przez"],
                             "Data zwrotu": row["Data zwrotu"],
                             "Zarezerwowane przez": row["Zarezerwowane przez"]})

    os.remove("katalog.csv")
    os.rename("katalog_new.csv", "katalog.csv")
    print("Ksiazka zostala usunieta z katalogu.")


def przegladaj_katalog():
    print("Przegladaj wedlug kolumny: ")
    menu({"Tytul": (przegladaj_po, '0' , {}),
          "Autor": (przegladaj_po, '1', {}),
          "Slowa kluczowe": (przegladaj_po, '2' , {})
          })

def przegladaj_po(kolumna):
    kolumna = int(kolumna)
    fraza = input("Wpisz szukana fraze: ")
    with open("katalog.csv", "r", newline="") as catalog:
        headers = ["Tytul", "Autor", "Slowa kluczowe", "Wypozyczone przez", "Data zwrotu", "Zarezerwowane przez"]
        kolumna = headers[kolumna]
        next(catalog, None) #skip header
        print("Wyniki wyszukiwania: \n")
        n = 0
        for row in csv.DictReader(catalog, delimiter=',', fieldnames=headers):
            if fraza.lower() in row[kolumna].lower():
                print(n+1,".", row)
                n+=1
        if n==0:
            print("Nie znaleziono")


def ocen_poprawnosc_akcji(akcja, nick, wypozyczone_przez, data_zwrotu, rezerwacja):

    poprawna = True
    wiadomosc = ""

    if akcja=="prolonguj":
        if wypozyczone_przez != nick:
            poprawne = False
            wiadomosc = "Ta ksiazka nie jest wypozyczona prze Ciebie. Nie mozesz prolongowac."
        else:
            if data_zwrotu != str(datetime.date(9999,1,1)):
                poprawna = 1
                wiadomosc="Termin oddania prolongowany o miesiac."
            else:
                poprawna = 0
                wiadomosc = "Ta ksiazka nie jest wypozyczona."

    if akcja=="wypozycz":
        if data_zwrotu == str(datetime.date(9999,1,1)):
            poprawna = 1
            wiadomosc="Ksiazka wypozyczona."
        else:
            wiadomosc = "Ksiazka jest juz obecnie wypozyczona."

    if akcja == "rezerwuj":
        if rezerwacja == "-":
            poprawna = 1
            wiadomosc="Ksiazka zarezerwowana"
        else:
            poprawna = 0
            if rezerwacja == nick:
                wiadomosc = "Posiadasz już rezerwację na te ksiazke"
            else:
                wiadomosc = "Ksiazka jest juz zarezerwowana przez kogos innego. Sprobuj pozniej."


    if akcja=="przyjmij":
        if data_zwrotu != str(datetime.date(9999,1,1)):
            poprawna = 1
            wiadomosc = "Ksiazka zwrocona."
        else:
            poprawna = 0
            wiadomosc = "Ta ksiazka nie jest wypozyczona."

    return poprawna, wiadomosc


def aktualizuj_dane_ksiazki(tytul, autor, wypozyczone_przez, data_zwrotu, rezerwacja, akcja, nick):
    
    with open("katalog.csv", "r", newline="") as catalog_in, open('katalog_new.csv', "w", newline="") as catalog_out:

        pozycja_istnieje = False
        headers = ["Tytul", "Autor", "Slowa kluczowe", "Wypozyczone przez", "Data zwrotu", "Zarezerwowane przez"]
        writer = csv.DictWriter(catalog_out, fieldnames=headers)
        writer.writeheader()
        for row in csv.DictReader(catalog_in, delimiter=','):
            if row["Tytul"].lower() == tytul.lower() and row["Autor"].lower() == autor.lower():

                pozycja_istnieje = True
                katalog_wypozyczone_przez = row["Wypozyczone przez"]
                katalog_data_zwrotu = row["Data zwrotu"]
                katalog_rezerwacja = row["Zarezerwowane przez"]


                poprawna_akcja = ocen_poprawnosc_akcji(akcja, nick, katalog_wypozyczone_przez,
                                                       katalog_data_zwrotu, katalog_rezerwacja)[0]
                wiadomosc = ocen_poprawnosc_akcji(akcja, nick, katalog_wypozyczone_przez,
                                                       katalog_data_zwrotu, katalog_rezerwacja)[1]

                if poprawna_akcja:

                    if not rezerwacja:
                        rezerwacja = row["Zarezerwowane przez"]

                    if wypozyczone_przez==0:
                        wypozyczone_przez = row["Wypozyczone przez"]

                    writer.writerow({"Tytul": row["Tytul"],
                                     "Autor": row["Autor"],
                                     "Slowa kluczowe": row["Slowa kluczowe"],
                                     "Wypozyczone przez": wypozyczone_przez,
                                     "Data zwrotu": data_zwrotu,
                                     "Zarezerwowane przez": rezerwacja
                    })
                else:
                    writer.writerow({"Tytul": row["Tytul"],
                                     "Autor": row["Autor"],
                                     "Slowa kluczowe": row["Slowa kluczowe"],
                                     "Wypozyczone przez": row["Wypozyczone przez"],
                                     "Data zwrotu": row["Data zwrotu"],
                                     "Zarezerwowane przez": row["Zarezerwowane przez"]})

            else:
                writer.writerow({"Tytul": row["Tytul"],  # DRY
                                 "Autor": row["Autor"],
                                 "Slowa kluczowe": row["Slowa kluczowe"],
                                 "Wypozyczone przez": row["Wypozyczone przez"],
                                 "Data zwrotu": row["Data zwrotu"],
                                 "Zarezerwowane przez": row["Zarezerwowane przez"]})

    os.remove("katalog.csv")
    os.rename("katalog_new.csv", "katalog.csv")

    if pozycja_istnieje==0:
        wiadomosc = "Taka pozycja nie istnieje w katalogu."

    print(wiadomosc)


def prolonguj_ksiazke(nick):

    tytul = input("Podaj tytuł: ")
    autor = input("Podaj autora: ")

    aktualizuj_dane_ksiazki(tytul=tytul, autor=autor, wypozyczone_przez=nick, data_zwrotu=datetime.date(year, month, day),
                            rezerwacja=0,
                            akcja="prolonguj", nick=nick)


def przyjmij_zwrot():

    tytul = input("Podaj tytuł: ")
    autor = input("Podaj autora: ")

    aktualizuj_dane_ksiazki(tytul=tytul, autor=autor, wypozyczone_przez="-",
                            data_zwrotu=str(datetime.date(9999, 1, 1)),
                            rezerwacja=0,
                            akcja="przyjmij", nick="-")

def rezerwuj_ksiazke(nick):

    tytul = input("Podaj tytul: ")
    autor = input("Podaj autora: ")

    aktualizuj_dane_ksiazki(tytul=tytul, autor=autor, wypozyczone_przez=0,
                            data_zwrotu=datetime.date(year, month, day),
                            rezerwacja=nick,
                            akcja="rezerwuj", nick=nick)


def wypozycz_ksiazke(nick):

    tytul = input("Podaj tytuł: ")
    autor = input("Podaj autora: ")

    aktualizuj_dane_ksiazki(tytul, autor, nick, datetime.date(year, month, day), 0, "wypozycz", nick)


def bibliotekarz():
    while True:
        menu({"Przyjmij zwrot książki": (przyjmij_zwrot, (), {}),
              "Dodaj nową książkę": (dodaj_ksiazke, (), {}),
              "Usuń książkę": (usun_ksiazke, (), {}),
              "Przeglądaj katalog": (przegladaj_katalog, (), {}),
              "Wyjdź": (library, (), {})
              })

def user():
    nick = input("Podaj swój nickname: ")
    while True:
        menu({"Wypożycz książkę": (wypozycz_ksiazke, [nick], {}),
              "Zarezerwuj książkę": (rezerwuj_ksiazke, [nick], {}),
              "Prolonguj książkę": (prolonguj_ksiazke, [nick], {}),
              "Przegladaj katalog": (przegladaj_katalog, (), {}),
              "Wyjdź": (library, (), {})
          })

def library():
    print("Witaj. Kim jesteś?")
    menu({"Bibliotekarzem": (bibliotekarz, (), {}),
          "Użytkownikiem": (user, (), {})
          })


library()
