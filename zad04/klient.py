import win32pipe
import win32file

def client():
    client_queue = win32file.CreateFile(
        r'\\.\pipe\server_queue',
        win32file.GENERIC_READ | win32file.GENERIC_WRITE,
        0,
        None,
        win32file.OPEN_EXISTING,
        0,
        None
    )

    win32pipe.SetNamedPipeHandleState(
        client_queue,
        win32pipe.PIPE_READMODE_MESSAGE,
        None,
        None
    )

    while True:
        requested_id = input("Podaj ID: ")
        win32file.WriteFile(client_queue, requested_id.encode())
        response = win32file.ReadFile(client_queue, 65536)[1].decode()
        print(f"Odpowiedź: {response}")

if __name__ == "__main__":
    try:
        client()
    except KeyboardInterrupt:
        print("Klient zostaje zatrzymany...")
