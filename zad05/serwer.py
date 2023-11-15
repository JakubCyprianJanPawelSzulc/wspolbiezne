import sysv_ipc
import os
import time

def translate(word):
    dictionary = {"ogród":"garden", "siła":"force", "myć":"wash", }
    return dictionary.get(word, "Nie znam takiego słowa")

def main():
    input_queue_key=1993
    output_queue_key=1998

    input_queue = sysv_ipc.MessageQueue(input_queue_key, sysv_ipc.IPC_CREAT)
    output_queue = sysv_ipc.MessageQueue(output_queue_key, sysv_ipc.IPC_CREAT)

    while True:
        message, t = input_queue.receive()
        time.sleep(2)
        word = message.decode("utf-8")
        translation = translate(word)

        response = f"{os.getpid()}: {word} - {translation}"
        output_queue.send(response.encode("utf-8"), type=t)

if __name__ == "__main__":
    main()
