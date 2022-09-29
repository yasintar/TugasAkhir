import time
from threading import Thread
from random import randint

class Reader:
    def __init__(self, file) -> None:
        self.fopen = open(file,"r")
        self.readingThread = Thread(target=self.read, name="IntegerInput")
        self.num = None
        self.isStopped = False

    def getNum(self):
        return (self.num % 2)

    def read(self):
        while True:
            line = self.fopen.readline()
            if not line: break
            self.num = int(line)
            print(self.getNum())

            if self.isStopped : break

            time.sleep(1)

    def start(self):
        print("[]\tStart to read a File as Input")
        self.readingThread.start()

    def stop(self):
        print("[]\tStop to read a File as Input")
        self.isStopped = True
        time.sleep(1)
        self.readingThread.join()
        self.fopen.close()

class Creator:
    def __init__(self) -> None:
        pass

    def create(self):
        nums = []
        fopen = open("num.txt", "a")
        for _ in range(0,1000000):
            fopen.write(str(randint(0,100))+"\n")
    
if __name__=="__main__":
    # creator = Creator()
    # creator.create()
    fileReader = Reader("num.txt")
    try:
        fileReader.start()
    except KeyboardInterrupt:
        fileReader.stop()
    