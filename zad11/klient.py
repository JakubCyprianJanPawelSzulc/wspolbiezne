import tkinter as tk
from tkinter import messagebox
import threading
import time
import socket

class CrosswordClient:
    def __init__(self,root):
        self.root = root
        self.client_socket=self.create_communication_thread(12345)
        self.create_ui()

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

    def wait_for_response(self, row, col):
        while True:
            print("Waiting for response")
            time.sleep(1)
            response = self.receive_data(self.client_socket)
            print("Response:", response)
            if response is not None:
                if response == 'False':
                    self.entry_grid[row][col].delete(0, tk.END)
                    print("Invalid move")
                    break
                if response == 'True':
                    print("Valid move")
                    break
                else:
                    print("complete word in row: ", response)
                    self.block_row_and_color_green(int(response))
                    break
                    
    def block_row_and_color_green(self, row):
        for i in range(10):
            self.entry_grid[row][i].config(state=tk.DISABLED, bg='green')

    def receive_data(self, socket):
        data = socket.recv(1024).decode()
        print("Received data:", data)
        return data if data else None
    
    def update_crossword(self, response):
        for i, row in enumerate(response):
            for j, char in enumerate(row):
                self.entry_grid[i][j].delete(0, tk.END)
                self.entry_grid[i][j].insert(0, char)
                self.entry_grid[i][j].config(state=tk.DISABLED)

    def handle_click(self, row, col):
        if self.current_field:
            self.entry_grid[self.current_field[0]][self.current_field[1]].config(bg='white')

        self.current_field = (row, col)
        self.entry_grid[row][col].config(bg='lightblue')

    def handle_key(self, event):
        data = event.char
        row, col = self.current_field
        msg = f"{data}/{row}/{col}"
        self.send_data(msg)
        print("Sent data:", data, row, col)
        self.wait_for_response(row, col)

    def send_data(self, data):
        self.client_socket.sendall(data.encode())


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Crossword Client")

    client = CrosswordClient(root)

    root.mainloop()