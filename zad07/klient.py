import socket

def choice_func():
    choice = input("Wybierz (p/k/n) lub wpisz 'koniec' aby zakończyć grę: ")
    if choice.lower() not in ["p", "k", "n", "koniec"]:
        print("Niepoprawny wybór")
        return choice_func()
    return choice

def client(player_id):
    host = "127.0.0.1"
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    client_socket.sendto(f"start,{player_id}".encode(), (host, port))

    while True:
        choice = choice_func()

        client_socket.sendto(f"{choice},{player_id}".encode(), (host, port))

        if choice.lower() == "koniec":
            break

        result, _ = client_socket.recvfrom(1024)
        print(result.decode())

    client_socket.close()

if __name__ == "__main__":
    player_id = input("Podaj identyfikator gracza (123 lub 124): ")
    client(player_id)
