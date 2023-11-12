import os
import signal
import time

server_queue_path = "/tmp/server_queue"

def send_signal_to_server(signum):
    if not os.path.exists(server_queue_path):
        print("Nie można połączyć się z serwerem.")
        return
    # if signum == signal.SIGUSR1:
    #     print("Wysyłanie sygnału SIGUSR1. Koniec.")
    #     os.remove(server_queue_path)
    #     return
    with open(server_queue_path, 'w') as server_queue:
        server_queue.write(f"{signum}")

    

signal.signal(signal.SIGHUP, lambda signum, frame: send_signal_to_server(signum))
signal.signal(signal.SIGTERM, lambda signum, frame: send_signal_to_server(signum))
signal.signal(signal.SIGUSR1, lambda signum, frame: send_signal_to_server(signum))

def main():
    print("Program signalTest - wysyła sygnały do serwera.")

    while True:
        print("1. Wyślij sygnał SIGHUP")
        print("2. Wyślij sygnał SIGTERM")
        print("3. Wyślij sygnał SIGUSR1")
        print("0. Zakończ program")

        choice = input("Wybierz opcję: ")

        if choice == "1":
            send_signal_to_server(signal.SIGHUP)
        elif choice == "2":
            send_signal_to_server(signal.SIGTERM)
        elif choice == "3":
            send_signal_to_server(signal.SIGUSR1)
        elif choice == "0":
            break
        else:
            print("Nieprawidłowy wybór. Spróbuj ponownie.")

        time.sleep(1)

if __name__ == "__main__":
    main()
