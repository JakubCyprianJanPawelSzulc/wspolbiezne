import math
import time
from multiprocessing import Pool


def czy_pierwsza(k):
    for i in range(2, int(math.sqrt(k)) + 1):
        if k % i == 0:
            return False
    return True


def stworz_mlp(r):
    mlp = []
    s = math.ceil(math.sqrt(r))
    for i in range(2, s + 1):
        if czy_pierwsza(i):
            mlp.append(i)
    return mlp


def znajdz_pierwsze(l, r, mlp):
    primes = set()
    s = math.ceil(math.sqrt(r))
    for i in range(l, r + 1):
        for p in mlp:
            if i % p == 0:
                break
            if p * p > i:
                primes.add(i)
                break
        primes.add(i)
    return primes


if __name__ == '__main__':
    left = 1000000
    right = 2000000
    mlp = stworz_mlp(right)
    processes = 4

    print("Start sekwencyjnie")
    start1 = time.time()
    solution1 = znajdz_pierwsze(left, right, mlp)
    end1 = time.time() - start1
    print("Czas sekwencyjnie: ", end1)

    print("Start równolegle")
    with Pool(processes) as p:
        components = []
        part = (right - left) // processes
        for i in range(processes):
            components.append([left + i * part, left + (i + 1) * part, mlp])
        start2 = time.time()
        solution2 = p.starmap(znajdz_pierwsze, components)
        end2 = time.time() - start2

    print("Czas równolegle: ", end2)
    print("O ile lepsze: ", end1 / end2)
    print("Czy poprawne rozwiązanie: ", solution1 == set.union(*solution2))