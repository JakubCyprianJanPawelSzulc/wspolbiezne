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

        connected_users=0

        client1_socket = None
        client2_socket = None
        client1_address = None
        client2_address = None

        while connected_users < 2:
            client_socket, client_address = server_socket.accept()
            print('New connection from', client_address)
            connected_users += 1
            if client1_socket is None:
                client1_socket = client_socket
                client1_address = client_address
            else:
                client2_socket = client_socket
                client2_address = client_address

        print('Both players connected')
        self.respond_to_player(client1_socket, True, None, self.board)
        self.wait_for_response(client1_socket, client2_socket)
            

    def wait_for_response(self, client_socket1, client_socket2):
        current_socket=client_socket1
        while True:
            # time.sleep(1)
            response = self.get_response_from_player(current_socket)
            if response is not None:
                is_good, index = self.process_response(response)
                self.respond_to_player(current_socket, is_good, index, self.board)
                if is_good is False:
                    if current_socket == client_socket1:
                        current_socket = client_socket2
                        print("Switching to player 2")
                        print("Current socket:", current_socket)
                        self.respond_to_player(current_socket, True, None, self.board)
                    else:
                        current_socket = client_socket1
                        print("Switching to player 1")
                        print("Current socket:", current_socket)
                        self.respond_to_player(current_socket, True, None, self.board)


    def get_response_from_player(self, client_socket):
        with self.lock:
            response = client_socket.recv(1024).decode()
            print("Received data:", response)
            return response if response else None
        
    def respond_to_player(self, client_socket, isGood, isCompleteWord, boardState):
        msg = f"{isGood}/{isCompleteWord}/{boardState}/"
        client_socket.sendall(msg.encode())

    def check_if_word_completed(self):
        for i in range(len(self.board)):
            if self.complete_words[i]:
                continue
            if self.board[i] == self.target_board[i]:
                self.complete_words[i] = True
                return True, i
        return False, None 

    def process_response(self, response):
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
                        return True, index
                    else:
                        return True, None
                else:
                    print(f"Player guessed incorrectly: {letter} at position ({x}, {y})")
                    return False, None
            except ValueError:
                print("Invalid response format")

    def validate_move(self, letter, x, y):
        return (
            x >= 0 and x < len(self.board) and
            y >= 0 and y < len(self.board[x]) and
            self.board[x][y] == '' and
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
