import os
import sys
import json
import time
import threading
import signal

server_queue_path = "/tmp/server_queue"
database = {1: "Podolski", 2: "Klose", 3: "Mueller", 4: "Ballack"}
message_lock = threading.Lock()

def handle_client_request(client_queue_path, client_id, requested_ID):
    time.sleep(3)
    try:
        if requested_ID in database:
            response = database[requested_ID]
        else:
            response = "Nie ma"

        with open(client_queue_path, 'w') as client_queue:
            with message_lock:
                client_queue.write(response)

    except Exception as e:
        print(f"Obsługa klienta {client_id} nie powiodła się: {e}")

def handle_signals(signum,frame):
    if signum == signal.SIGTERM or signum == signal.SIGHUP:
        print(f"otrzymano sygnał {signum}")
    elif signum == signal.SIGUSR1:
        print("otrzymano sygnał SIGUSR1. Koniec.")

def main():
    signal.signal(signal.SIGTERM, handle_signals)
    signal.signal(signal.SIGHUP, handle_signals)
    signal.signal(signal.SIGUSR1, handle_signals)

    if not os.path.exists(server_queue_path):
        os.mkfifo(server_queue_path)

    while True:
        with open(server_queue_path, 'r') as server_queue:
            data = server_queue.read().strip()

            try:
                request = json.loads(data)

                if isinstance(request, dict):
                    client_queue_path = request['client_queue_path']
                    client_id = request['client_id']
                    requested_id = request['ID']

                    thread = threading.Thread(target=handle_client_request, args=(client_queue_path, client_id, requested_id))
                    thread.start()
                else:
                    print(f"Otrzymano sygnał: {data}")
                    if data == "10":
                        sys.exit(0)
                    if data == "1":
                        print("Otrzymano sygnał SIGHUP")
                    elif data == "15":
                        print("Otrzymano sygnał SIGTERM")

            except json.JSONDecodeError:
                print(f"Otrzymano sygnał: {data}")
if __name__ == "__main__":
    main()
