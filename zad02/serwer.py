import os
import time

def main():
    while True:
        lockfile = "serverLockFile.lock"
        if os.path.exists(lockfile):
            clientFile = ""
            with open("serverInputFile.txt", "r") as file:
                clientFile = file.readline().strip()
            if not clientFile:
                continue
            with open("serverInputFile.txt", "r") as serverInputFile:
                print("Tekst klienta:")
                for line in serverInputFile:
                    print(line, end="")
                with open(clientFile, "w") as clientFile:
                    while True:
                        line = input("Podaj linię do pliku dla klienta (esc aby zakończyć): ")
                        if line == "esc":
                            break
                        clientFile.write(line + "\n")
            os.remove(lockfile)
        else:
            time.sleep(1)
            continue

if __name__ == "__main__":
    main()
