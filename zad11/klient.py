import socket

def connect_to_server(port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', port))
    print('Connected to server on port', port)
    return client_socket

def close_connection(socket):
    socket.close()
    print('Connection closed')

def receive_data(socket):
    data = socket.recv(1024).decode()
    return data

def send_data(socket, data):
    socket.send(data.encode())

if __name__ == '__main__':
    try:
        client_socket = connect_to_server(12345)
        while True:
            message = input('Enter message: ')
            send_data(client_socket, message)
            response = receive_data(client_socket)
            print('Received response:', response)

    except KeyboardInterrupt:
        close_connection(client_socket)
        