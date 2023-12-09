import threading

def sumuj_podliste(lista, start, koniec, lock, wyniki):
    suma = sum(lista[start:koniec])
    with lock:
        wyniki.append(suma)

def sumuj_rekurencyjnie(lista, start, koniec, ilosc_watkow, lock, wyniki):
    if ilosc_watkow == 1:
        sumuj_podliste(lista, start, koniec, lock, wyniki)
    else:
        srodek = (start + koniec) // 2

        watki = []
        for i in range(2):
            nowy_start = start if i == 0 else srodek
            nowy_koniec = srodek if i == 0 else koniec
            watek = threading.Thread(target=sumuj_rekurencyjnie, args=(lista, nowy_start, nowy_koniec, ilosc_watkow // 2, lock, wyniki))
            watki.append(watek)
            watek.start()

        for watek in watki:
            watek.join()

def main():
    lista_liczb = list(range(1, 1000001))

    ilosc_watkow = 4

    lock = threading.Lock()

    wyniki_czesciowe = []

    sumuj_rekurencyjnie(lista_liczb, 0, len(lista_liczb), ilosc_watkow, lock, wyniki_czesciowe)

    suma_koncowa = sum(wyniki_czesciowe)

    print(f"Suma wszystkich elementów: {suma_koncowa}")

if __name__ == "__main__":
    main()
