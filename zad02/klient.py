import os
import time

def client():
    serverLockFile = "serverLockFile.lock"
    clientFile = input("Podaj nazwę swojego pliku: ")
    while True:
        if not os.path.exists(clientFile):
            with open(clientFile, "w") as file:
                pass
        with open(clientFile, "r") as clientInput:
            if os.stat(clientFile).st_size == 0:
                pass
            else:
                print("Odpowiedź serwera:")
                for line in clientInput:
                    print(line, end="")
                break
        if os.path.exists(serverLockFile):
            print("Serwer zajęty")
            time.sleep(3)
            continue
        with open(serverLockFile, "w") as file:
            file.write("lock")

        serverInputFile = "serverInputFile.txt"
        with open(serverInputFile, "w") as file:
            file.write(clientFile + "\n")
            while True:
                line = input("Podaj linię do pliku dla serwera (esc aby zakończyć): ")
                if line == "esc":
                    break
                file.write(line + "\n")


if __name__ == "__main__":
    client()
