import math
import threading
from threading import Barrier

l = 2
r = 200
num_threads = 5

def pierwsza(k):
    s = math.ceil(math.sqrt(k))
    for i in range(2, s + 1):
        if k % i == 0:
            return False
    return True

def find_primes_in_range(lock, start, end, barrier_start, barrier_end, result_list):
    local_primes = []
    for i in range(start, end + 1):
        if pierwsza(i):
            local_primes.append(i)
    barrier_start.wait()

    with lock:
        result_list.extend(local_primes)

    barrier_end.wait()

barrier_start = Barrier(num_threads + 1) 
barrier_end = Barrier(num_threads)

threads = []
primes = []

lock = threading.Lock()

for i in range(num_threads):
    start = l + i * ((r - l + 1) // num_threads)
    end = start + ((r - l + 1) // num_threads) - 1

    if i == num_threads - 1:
        end = r

    thread = threading.Thread(target=find_primes_in_range, args=(lock, start, end, barrier_start, barrier_end, primes))
    threads.append(thread)

for thread in threads:
    thread.start()

barrier_start.wait()

barrier_end.wait()

print(primes)
