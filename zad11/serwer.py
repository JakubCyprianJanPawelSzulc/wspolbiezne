import socket
import threading
import time

class CrosswordGame:
    def __init__(self, words):
        self.words = words
        self.current_word_index = 0
        self.current_word = self.words[self.current_word_index]
        self.lock = threading.Lock()

        self.board = [[''] * len(self.current_word) for _ in range(len(self.words))]

    def start_server(self, port):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', port))
        server_socket.listen()
        print('Server is listening on port', port)

        client_socket, client_address = server_socket.accept()
        print('Client connected from', client_address)

        self.wait_for_response(client_socket)

    def wait_for_response(self, client_socket):
        while True:
            time.sleep(1)
            response = self.get_response_from_player(client_socket)
            if response is not None:
                self.update_crossword(response)
                if self.is_word_completed():
                    print("Word completed!")
                    self.current_word_index += 1
                    if self.current_word_index < len(self.words):
                        self.current_word = self.words[self.current_word_index]

    def get_response_from_player(self, client_socket):
        with self.lock:
            response = client_socket.recv(1024).decode()
            print("Received data:", response)
            return response if response else None

    def update_crossword(self, response):
        with self.lock:
            for i, char in enumerate(response):
                self.board[self.current_word_index][i] = char

    def is_word_completed(self):
        with self.lock:
            return '' not in self.board[self.current_word_index]

if __name__ == '__main__':
    der_port = 12345

    words = ["PYTHON", "JAVA", "ANDRZEJ", "JACEK", "METANABOL", "DIANABOL", "STERYDY", "BMW", "ZAZA", "CRACK"]

    game = CrosswordGame(words)
    game.start_server(der_port)
