import time
import math
from multiprocessing import Pool, Manager

l = 1000000
r = 2000000

def pierwsza(k):
 for i in range (2,k-1):
   if i*i>k:
     return True
   if k%i == 0:
     return False
 return True


def pierwsza1(k,mlp):
 for p in mlp:
   if k%p == 0:
     return False
   if p*p>k:
     return True
 return True


def licz(l,r):
  mlp = []
  s = math.ceil(math.sqrt(r))
  for i in range (2,s+1):
    if pierwsza(i):
       mlp.append(i)
  pierwsze = []
  for i in range (l,r+1):
    if pierwsza1(i,mlp):
       pierwsze.append(i)
    return pierwsze
  
def blizniacze_sekwencyjnie(l,r):
  pierwsze = []
  for i in range (l,r+1):
    if pierwsza(i) and pierwsza(i+2):
       pierwsze.append((i,i+2))
  return pierwsze

def blizniacze_rownolegle_pomocnicza(chunk, shared_list):
    result = blizniacze_sekwencyjnie(chunk[0], chunk[1])
    shared_list.extend(result)

def blizniacze_rownolegle(l, r):
    with Manager() as manager:
        shared_list = manager.list()
        pool = Pool()
        chunks = [(i, i + 10000) for i in range(l, r + 1, 10000)]
        pool.starmap(blizniacze_rownolegle_pomocnicza, [(chunk, shared_list) for chunk in chunks])
        pool.close()
        pool.join()
        return list(shared_list)

def main():
    start = time.time()
    wynik1 = blizniacze_sekwencyjnie(l,r)
    end = time.time()
    print("Czas sekwencyjnie: ",end - start)
    start = time.time()
    wynik2 = blizniacze_rownolegle(l,r)
    end = time.time()
    print("Czas rownolegle: ",end - start)
    # print("porównanie wyników: ", wynik1 == wynik2)
    # print("wynik1: ", len(wynik1))
    # print("wynik2: ", len(wynik2))

if __name__ == '__main__':
    main()
