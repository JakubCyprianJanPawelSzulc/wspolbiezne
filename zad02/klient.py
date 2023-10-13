import os
import time

def client():
    serverLockFile = "serverLockFile.lock"
    while True:
        if os.path.exists(serverLockFile):
            print("Serwer zajęty")
            time.sleep(3)
            continue
        with open (serverLockFile, "w") as file:
            file.write("lock")
        
        serverInputFile="serverInputFile.txt"

        with open(serverInputFile, "r") as serverInput:
            for line in serverInput:
                print(line, end="")
        response = input("Podaj odpowiedź dla serwera (Esc aby zakończyć): ")
        if response == "Esc":
            break
            

if __name__ == "__main__":
    client()
