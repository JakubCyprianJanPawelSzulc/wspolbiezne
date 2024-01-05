import socket
import threading
import time

class CrosswordGame:
    def __init__(self, words):
        self.words = words
        self.lock = threading.Lock()
        self.target_board = []
        self.board = [[''] * len(word) for word in words]
        self.complete_words = [False] * len(words)

    def initialize_target_board(self, words):
        board = [[''] * len(word) for word in words]
        for i, word in enumerate(words):
            for j, letter in enumerate(word):
                board[i][j] = letter
        self.target_board = board
    
    def print_board(self, board):
        for row in board:
            print(row)
        print()

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
                self.process_response(response, client_socket)
                

    def get_response_from_player(self, client_socket):
        with self.lock:
            response = client_socket.recv(1024).decode()
            print("Received data:", response)
            return response if response else None
        
    def respond_to_player(self, client_socket, isGood, isCompleteWord):
        if isGood:
            if isCompleteWord is not None:
                client_socket.send(str(isCompleteWord).encode())
            else:
                client_socket.send('True'.encode())
        else:
            client_socket.send('False'.encode())

    def check_if_word_completed(self):
        for i in range(len(self.board)):
            if self.complete_words[i]:
                continue
            if self.board[i] == self.target_board[i]:
                self.complete_words[i] = True
                return True, i
        return False, None 

    def process_response(self, response, client_socket):
        with self.lock:
            try:
                letter, x, y = response.split('/')
                x, y = int(x), int(y)
                if self.validate_move(letter, x, y):
                    self.update_board(letter, x, y)
                    print(f"Player guessed correctly: {letter} at position ({x}, {y})")
                    self.print_board(self.board)
                    completed, index = self.check_if_word_completed()
                    if completed:
                        print(f"Player completed word: {self.words[index]}")
                        self.respond_to_player(client_socket, True, index)
                    else:
                        self.respond_to_player(client_socket, True, None)
                else:
                    print(f"Player guessed incorrectly: {letter} at position ({x}, {y})")
                    self.respond_to_player(False, client_socket)
            except ValueError:
                print("Invalid response format")

    def validate_move(self, letter, x, y):
        return (
            0 <= x < len(self.target_board) and
            0 <= y < len(self.target_board[0]) and
            self.target_board[x][y] == letter
        )
    
    def update_board(self, letter, x, y):
        self.board[x][y] = letter

if __name__ == '__main__':
    der_port = 12345

    words = ["PYTHON", "JAVA", "ANDRZEJ", "BAZA", "METANABOL", "DIANABOL", "STERYDY", "SIGMA", "ZAZA", "CRACK"]

    game = CrosswordGame(words)
    game.initialize_target_board(words)
    game.print_board(game.target_board)
    game.start_server(der_port)
