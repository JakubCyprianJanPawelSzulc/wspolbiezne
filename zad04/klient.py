import win32pipe
import win32file

def client(id):
    server_queue = win32file.CreateFile(
        r'\\.\pipe\server_queue',
        win32file.GENERIC_READ | win32file.GENERIC_WRITE,
        0,
        None,
        win32file.OPEN_EXISTING,
        0,
        None
    )

    my_queue = win32pipe.CreateNamedPipe(
        r'\\.\pipe\client_queue_' + id,
        win32pipe.PIPE_ACCESS_DUPLEX,
        win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
        1, 65536, 65536,
        0,
        None
    )

    win32pipe.SetNamedPipeHandleState(
        server_queue,
        win32pipe.PIPE_READMODE_MESSAGE,
        None,
        None
    )

    requested_id = input("Podaj poszukiwane ID (lub 'exit' aby zakończyć): ")
    message = id + ':' + requested_id
    win32file.WriteFile(server_queue, message.encode())

    while True:
        try:
            win32pipe.ConnectNamedPipe(my_queue, None)
            response = win32file.ReadFile(my_queue, 65536)[1].decode()
            print(f"Odpowiedź: {response}")
            break
        except:
            pass
        

if __name__ == "__main__":
    try:
        id = input("podaj swoje ID:")
        client(id)
    except KeyboardInterrupt:
        print("Klient zostaje zatrzymany...")
