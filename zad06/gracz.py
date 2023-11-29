import sysv_ipc
import time

NULL_CHAR = '\0'

def write_to_memory(mem, data):
    data += NULL_CHAR
    data = data.encode()
    mem.write(data)

def read_from_memory(mem):
    data = mem.read()
    data = data.decode()
    index = data.find(NULL_CHAR)
    if index != -1:
        data = data[:index]
    return data

def play_game(cards, player_semaphore, opponent_semaphore, is_first, player_memory, opponent_memory):
    for round_num in range(1, 4):
        print(f"\nRunda {round_num}")

        # wybór karty
        chosen_card = input("Wybierz kartę (A, B, lub C): ").upper()
        while chosen_card not in cards:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")
            chosen_card = input("Wybierz kartę (A, B, lub C): ").upper()

        print(f"Twój wybór w rundzie {round_num}: {chosen_card}")

        # zapis wyboru do pamięci współdzielonej i zwolnienie semafora dla przeciwnika
        write_to_memory(player_memory, chosen_card)
        opponent_semaphore.release()
        player_semaphore.acquire()

        # odczyt wyboru przeciwnika z pamięci współdzielonej
        opponent_choice = read_from_memory(opponent_memory)
        print(f"Wybór przeciwnika w rundzie {round_num}: {opponent_choice}")

        # zwolnienie semafora dla przeciwnika i pobranie semafora dla siebie
        opponent_semaphore.release()
        player_semaphore.acquire()

        # sprawdzenie kto wygrał rundę
        if (is_first and opponent_choice == chosen_card) or (not is_first and opponent_choice != chosen_card):
            print("------Wygrałeś tę rundę!------")
        else:
            print("------Przegrałeś tę rundę.------")

    if is_first:
        print("\n------Koniec gry. Wygrałeś!------")
    else:
        print("\n------Koniec gry. Przegrałeś.------")

    sysv_ipc.remove_shared_memory(player_memory.id)
    sysv_ipc.remove_shared_memory(opponent_memory.id)
    sysv_ipc.remove_semaphore(player_semaphore.id)
    sysv_ipc.remove_semaphore(opponent_semaphore.id)


key = 13
cards = ['A', 'B', 'C']

try:
    player_semaphore = sysv_ipc.Semaphore(key, sysv_ipc.IPC_CREX, 0o700, 0)
    is_first_player = True
except sysv_ipc.ExistentialError:
    player_semaphore = sysv_ipc.Semaphore(key)
    is_first_player = False
    time.sleep(0.1)

if is_first_player:
    player_memory = sysv_ipc.SharedMemory(key, sysv_ipc.IPC_CREX)
    opponent_memory = sysv_ipc.SharedMemory(key + 1, sysv_ipc.IPC_CREX)
    opponent_semaphore = sysv_ipc.Semaphore(key + 1, sysv_ipc.IPC_CREX, 0o700, 0)
    play_game(cards, player_semaphore, opponent_semaphore, is_first_player, player_memory, opponent_memory)
else:
    player_semaphore = sysv_ipc.Semaphore(key)
    opponent_semaphore = sysv_ipc.Semaphore(key + 1)
    player_memory = sysv_ipc.SharedMemory(key)
    opponent_memory = sysv_ipc.SharedMemory(key + 1)
    play_game(cards, opponent_semaphore, player_semaphore, is_first_player, opponent_memory, player_memory)
