import win32pipe
import win32file
import os

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

def server():
    if not os.path.exists('database.txt'):
        create_database()

    server_queue = win32pipe.CreateNamedPipe(
        r'\\.\pipe\server_queue',
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None
    )

    win32pipe.ConnectNamedPipe(server_queue, None)

    while True:
        requested_id = win32file.ReadFile(server_queue, 65536)[1].decode()
        print(f"Otrzymano zapytanie o ID: {requested_id}")

        response = lookup_id(int(requested_id))
        print(f"Odpowiedź: {response}")

        win32file.WriteFile(server_queue, response.encode())


if __name__ == "__main__":
    try:
        server()
    except KeyboardInterrupt:
        print("Serwer zostaje zatrzymany...")
