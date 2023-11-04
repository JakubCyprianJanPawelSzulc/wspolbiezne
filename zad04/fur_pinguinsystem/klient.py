import os
import json

server_queue_path = "/tmp/server_queue"
client_queue_path = f"/tmp/client_queue_{os.getpid()}"
client_id = os.getpid()

id_for_request = input("Podaj ID: ")
try:
    id_for_request = int(id_for_request)
except ValueError:
    print("ID musi być liczbą!")
    exit(1)

request = {
    'ID': id_for_request,
    'client_queue_path': client_queue_path,
    'client_id': client_id
}

if not os.path.exists(client_queue_path):
    os.mkfifo(client_queue_path)

with open(server_queue_path, 'w') as server_queue:
    server_queue.write(json.dumps(request))

with open(client_queue_path, 'r') as client_queue:
    response = client_queue.read()

print(f"Odpowiedź od serwera: {response}")

os.remove(client_queue_path)
