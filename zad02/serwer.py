import os
import time

def main():
    while True:
        lockfile="serverLockFile.lock"
        if os.path.exists(lockfile):
            time.sleep(1)
            continue
        with open(lockfile, "w") as file:
            file.write("lock")
        
        with open("serverInputFile.txt", "w") as inputFile:
            clientFile = input("podaj nazwę pliku klienta: ")
            while True:
                line = input ("Podaj linię do pliku dla klienta (Esc aby zakończyć): ")
                if line == "Esc":
                    break
                inputFile.write(line+"\n")
        os.remove(lockfile)

        with open(clientFile, "r") as clientInput:
            print("Tekst klienta")
            for line in clientFile:
                print(line, end="")

        with open (lockfile, "w") as file:
            file.write("unlocked")

if __name__ == "__main__":
    main()
