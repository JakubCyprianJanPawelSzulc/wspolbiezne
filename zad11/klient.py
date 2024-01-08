import tkinter as tk
from tkinter import messagebox
import threading
import time
import socket
import ast

class CrosswordClient:
    def __init__(self,root):
        self.root = root
        self.client_socket=self.create_communication_thread(12345)
        self.create_ui()
        self.already_guessed = []
        self.waiting_for_response = False
        self.lock = threading.Lock()
        self.blocked=False
        self.wait_for_response()
        self.wait_for_response()

    def create_ui(self):
        self.entry_grid = [[None] * 10 for _ in range(10)]
        self.current_field = None

        for i in range(10):
            for j in range(10):
                entry = tk.Entry(self.root, width=2, justify="center", state=tk.NORMAL)
                entry.grid(row=i, column=j)
                entry.bind('<Button-1>', lambda event, row=i, col=j: self.handle_click(row, col))
                self.entry_grid[i][j] = entry
        self.root.bind('<Key>', self.handle_key)

    
    def create_communication_thread(self, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', port))
        print('Connected to server on port', port)
        return client_socket

    def wait_for_response(self):
        while True:
            print("Waiting for response")
            # time.sleep(1)
            response = self.receive_data(self.client_socket)
            print("Response:", response)
            if response.startswith("questions:"):
                print(response)
                break
            if response == 'None/None/None/None':
                print("Game over")
                if self.ask_for_rematch():
                    self.restart_game()
                else:
                    self.root.destroy()
                break

            if response is not None:
                parts = response.split('/')
                self.update_crossword(parts[2], parts[3])
                if parts[0] == 'True':
                    if self.blocked:
                        self.blocked=False
                        for i in range(10):
                            if i not in self.already_guessed:
                                for j in range(10):
                                    self.entry_grid[i][j].config(state=tk.NORMAL, bg='white')
                        break
                    if parts[1] == 'None':
                        print("Valid move")
                        self.waiting_for_response = False
                        break
                    elif int(parts[1]) not in self.already_guessed:
                        print("Complete word in row:", parts[1])
                        self.block_row_and_color_green(int(parts[1]))
                        self.waiting_for_response = False
                        break
                elif parts[0] == 'False':
                    print("Invalid move")
                    # self.entry_grid[row][col].delete(0, tk.END)
                    self.blocked=True
                    for i in range(10):
                        for j in range(10):
                            self.entry_grid[i][j].config(state=tk.DISABLED)
                    self.waiting_for_response = True
                    time.sleep(0.5)
                    # break

    def ask_for_rematch(self):
        print("Asking for rematch")
        answer = messagebox.askyesno("Rematch", "Do you want to play again?")
        if answer:
            self.send_data("True")
            return True
        else:
            self.send_data("False")
    
    def restart_game(self):
        self.already_guessed = []
        self.waiting_for_response = False
        self.blocked=False
        for i in range(10):
            for j in range(10):
                self.entry_grid[i][j].config(state=tk.NORMAL, bg='white')
                self.entry_grid[i][j].delete(0, tk.END)
        self.wait_for_response()


    def block_row_and_color_green(self, row):
        self.already_guessed.append(row)
        for i in range(10):
            self.entry_grid[row][i].config(state=tk.DISABLED)

    def receive_data(self, socket):
        # with self.lock:
            response = socket.recv(1024).decode()
            print("Received data:", response)
            return response if response else None
    
    def update_crossword(self, response, complete_words):
        print("Updating crossword")
        if response.endswith("True"):
            response = response[:-4]
        inner_list_strings = response[2:-2].split("], [")
        result = [s.split(", ") for s in inner_list_strings]
        result = [sublist + [''] * (10 - len(sublist)) for sublist in result]
        result = [[s[1:-1] for s in sublist] for sublist in result]
        self.root.after(0, self.update_entries, result)

        complete_words = ast.literal_eval(complete_words)
        for i in range(10):
            if complete_words[i]:
                self.root.after(0, lambda i=i: self.block_row_and_color_green(i))

    def update_entries(self, result):
        for i in range(10):
            for j in range(10):
                self.entry_grid[i][j].delete(0, tk.END)
                self.entry_grid[i][j].insert(0, result[i][j])
            

    def handle_click(self, row, col):
        if self.current_field:
            self.entry_grid[self.current_field[0]][self.current_field[1]].config(bg='white')

        self.current_field = (row, col)
        self.entry_grid[row][col].config(bg='lightblue')

    def handle_key(self, event):
        data = event.char.upper()
        if data.isalpha():
            row, col = self.current_field
            msg = f"{data}/{row}/{col}"
            self.send_data(msg)
            print("Sent data:", data, row, col)
            self.waiting_for_response = True
            self.wait_for_response()
        else:
            print("Invalid input")

    def send_data(self, data):
        self.client_socket.sendall(data.encode())


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Crossword Client")

    client = CrosswordClient(root)
    root.mainloop()