import os
import sys
import json
import time

server_queue_path = "/tmp/server_queue"
database = {1: "Podolski", 2: "Klose", 3: "Mueller", 4: "Ballack"}

def handle_client_request(client_queue_path, client_id, requested_ID):
    try:
        if requested_ID in database:
            response = database[requested_ID]
        else:
            response = "Nie ma"

        with open(client_queue_path, 'w') as client_queue:
            client_queue.write(response)

    except Exception as e:
        print(f"Obsługa klienta {client_id} nie powiodła się: {e}")

if not os.path.exists(server_queue_path):
    os.mkfifo(server_queue_path)

def main():
    while True:
        with open(server_queue_path, 'r') as server_queue:
            request = json.loads(server_queue.read())

        client_queue_path = request['client_queue_path']
        client_id = request['client_id']
        requested_id = request['ID']

        
        time.sleep(3)
        handle_client_request(client_queue_path, client_id, requested_id)

if __name__ == "__main__":
    main()
