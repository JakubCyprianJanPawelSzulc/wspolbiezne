import socket

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen()
    print('Server is listening on port', port)
    client_socket, client_address = server_socket.accept()
    print('Client connected from', client_address)
    return client_socket

def close_server(socket):
    socket.close()
    print('Server closed')

def receive_data(socket):
    data = socket.recv(1024).decode()
    return data

def send_data(socket, data):
    socket.send(data.encode())

if __name__ == '__main__':
    der_port = 12345
    server_socket = start_server(der_port)

    try:
        while True:
            received_data = receive_data(server_socket)
            print('Received data:', received_data)
            response=input('Enter response: ')
            send_data(server_socket, response)

    except KeyboardInterrupt:
        close_server(server_socket)
