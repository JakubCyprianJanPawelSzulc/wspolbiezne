import os

def main():
    while True:
        liczba = int(input("Podaj liczbę całkowitą: "))
        with open("dane.txt", "w") as file:
            file.write(str(liczba))
        while not os.path.exists("wyniki.txt"):
            pass
        with open("wyniki.txt", "r") as file:
            wynik = file.read()
            print("Odpowiedź od serwera:", wynik)
        os.remove("wyniki.txt")

if __name__ == "__main__":
    main()
