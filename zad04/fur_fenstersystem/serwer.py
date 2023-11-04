import win32pipe
import win32file
import os
import time
import pywintypes

database = {
    1: "Podolski",
    2: "Klose",
    3: "Mueller",
    4: "Ballack",
}

def create_database():
    with open('database.txt', 'w') as f:
        for k, v in database.items():
            f.write(str(k) + ':' + v + '\n')

def lookup_id(requested_id):
    with open('database.txt', 'r') as f:
        for line in f:
            if line.startswith(str(requested_id)):
                return line.split(':')[1].strip()
    return "Nie ma"

def handle_client(client_queue):
    while True:
        requested_id = win32file.ReadFile(client_queue, 65536)[1].decode()
        print(f"Otrzymano zapytanie o ID: {requested_id}")
        time.sleep(3)
        response = lookup_id(int(requested_id))
        print(f"Odpowiedź: {response}")
        win32file.WriteFile(client_queue, response.encode())

def server():

    while True:
        try:
            server_queue = win32pipe.CreateNamedPipe(
                r'\\.\pipe\server_queue',
                win32pipe.PIPE_ACCESS_DUPLEX,
                win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
                1, 65536, 65536,
                0,
                None
            )
            win32pipe.ConnectNamedPipe(server_queue, None)
            message = win32file.ReadFile(server_queue, 65536)[1].decode()
            client_id, requested_id = message.split(':')
            print(f"Otrzymano zapytanie o ID: {requested_id}")
            time.sleep(3)
            response = lookup_id(int(requested_id))
            print(f"Odpowiedź: {response}")
            client_response_queue = win32file.CreateFile(
                r'\\.\pipe\client_queue_' + client_id,
                win32file.GENERIC_READ | win32file.GENERIC_WRITE,
                0,
                None,
                win32file.OPEN_EXISTING,
                0,
                None
            )
            win32file.WriteFile(client_response_queue, response.encode())

        except pywintypes.error as e:
            if e.args[0] == 109:
                print("Klient zakończył połączenie")
            else:
                raise
        finally:
            win32file.CloseHandle(server_queue)

if __name__ == "__main__":
    try:
        server()
    except KeyboardInterrupt:
        print("Serwer zostaje zatrzymany...")
