import os

def oblicz_wynik(liczba):
    return liczba * liczba

def main():
    while True:
        while not os.path.exists("dane.txt"):
            pass
        with open("dane.txt", "r") as file:
            liczba = int(file.read())
        wynik = oblicz_wynik(liczba)
        with open("wyniki.txt", "w") as file:
            file.write(str(wynik))
        os.remove("dane.txt")

if __name__ == "__main__":
    main()
