import socket

def play_game(player1_choice, player2_choice):
    if player1_choice == player2_choice:
        return "Remis"
    elif (
        (player1_choice == "k" and player2_choice == "n")
        or (player1_choice == "n" and player2_choice == "p")
        or (player1_choice == "p" and player2_choice == "k")
    ):
        return "Gracz 1 wygrywa!"
    else:
        return "Gracz 2 wygrywa!"

def reset_scores():
    return {"123": 0, "124": 0}

def server():
    host = "127.0.0.1"
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))

    print("Serwer nasłuchuje na porcie", port)

    players = {}
    scores = reset_scores()

    counter = 0

    while True:
        data, addr = server_socket.recvfrom(1024)
        player_choice, player_id = data.decode().split(",")
        counter += 1
        print(counter)

        print("Otrzymano:", player_choice, player_id)
        players[player_id] = {"choice": player_choice, "addr": addr}

        if (counter <= 2) and (player_id not in players):
            print("Zapisano gracza", player_id)
        else:
            if counter >= 4:
                if counter % 2 == 0:
                    player1 = players["123"]
                    player2 = players["124"]
                    print("Grają:", player1["choice"], player2["choice"])

                    if player1["choice"].lower() == "koniec":
                        if player2["choice"].lower() == "koniec":
                            print("Obaj gracze zakończyli grę. Zerowanie punktacji i oczekiwanie na nową parę graczy.")
                            scores = reset_scores()
                            players = {}
                        else:
                            print(f"Gracz {player1['choice']} zakończył grę. Informowanie gracza {player2['choice']}.")
                            server_socket.sendto("koniec".encode(), player2["addr"])
                    elif player2["choice"].lower() == "koniec":
                        print(f"Gracz {player2['choice']} zakończył grę. Informowanie gracza {player1['choice']}.")
                        server_socket.sendto("koniec".encode(), player1["addr"])
                    else:
                        result = play_game(player1["choice"], player2["choice"])
                        server_socket.sendto(result.encode(), player1["addr"])
                        server_socket.sendto(result.encode(), player2["addr"])

if __name__ == "__main__":
    server()
