import sysv_ipc
import os
import random

class colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def main():
    input_queue_key=1993
    output_queue_key=1998

    input_queue = sysv_ipc.MessageQueue(input_queue_key, sysv_ipc.IPC_CREAT)
    output_queue = sysv_ipc.MessageQueue(output_queue_key, sysv_ipc.IPC_CREAT)

    word = input("Podaj słowo do przetłumaczenia: ")

    input_queue.send(word.encode('utf-8'), type=os.getpid())

    response, _ = output_queue.receive(type=os.getpid())
    print(f"{colors.YELLOW}Odpowiedź serwera:{colors.END}{response.decode('utf-8')}")

if __name__ == "__main__":
    main()
