import psutil
from threading import Thread
import time
from random import randint
from constant import *

class AGS():
    def __init__(self, withCPU, withRAM, withDisk, debug=True) -> None:
        self.withCPU = withCPU
        self.withRAM = withRAM
        self.withDisk = withDisk

        self.RAMWarning = False
        self.CPUWarning = False
        self.isWatchStopped = False
        self.counterUpthCPU = 1
        self.counterUpthRAM = 1
        self.timeToCapture = 1
        self.timeToProcess = 1

        if debug:
            self._cpu = None
            self._ram = None
            self._disk = None
        else:
            self._cpu = psutil.cpu_percent(0.1)
            self._ram = psutil.virtual_memory()[2]
            self._disk = psutil.disk_usage('/')[3]

    def getCurrentCPUStat(self):
        return self._cpu

    def getCurrentRAMStat(self):
        return self._ram

    def getCurrentDiskStat(self):
        return self._disk

    def getRAMWarning(self):
        return self.RAMWarning

    def getCPUWarning(self):
        return self.CPUWarning

    def getTimeToProcess(self):
        return self.timeToProcess
    
    def getTimeToCapture(self):
        return self.timeToCapture

    def setCurrentStat(self, cpu, ram, disk):
        self._cpu = cpu
        self._ram = ram
        self._disk = disk

    def watchCPU(self):
        print("[]\t(AGS) Watching CPU")
        while True:
            if self._cpu:
                if self._cpu > CONST_CPU and self._cpu < FULL_RESOURCE:
                    if self.CPUWarning : self.CPUWarning = False
                    self.timeToProcess = randint(1,5)*self.counterUpthCPU
                    self.counterUpthCPU = self.counterUpthCPU + 1
                elif self._cpu >= FULL_RESOURCE:
                    self.CPUWarning = True
                elif self._cpu < CONST_CPU:
                    if self.CPUWarning : self.CPUWarning = False
                    self.counterUpthCPU = 1
            
            if self.isWatchStopped:
                break

            time.sleep(TIMESLEEPTHREAD)

    def watchRAM(self):
        print("[]\t(AGS) Watching RAM")
        while True:
            if self._ram:
                if self._ram > CONST_RAM and self._ram < FULL_RESOURCE:
                    if self.RAMWarning : self.RAMWarning = False
                    self.timeToCapture = 1 + (1 - (CONST_RAM/100)) * self.counterUpthRAM
                elif self._ram >= FULL_RESOURCE:
                    self.RAMWarning = True
                elif self._ram < CONST_RAM:
                    self.counterUpthRAM = 1
                    if self.RAMWarning : self.RAMWarning = False

            if self.isWatchStopped:
                break

            time.sleep(TIMESLEEPTHREAD)

    def watchDisk(self):
        print("[]\t(AGS) Watching Disk")
        while True:
            if self._disk:
                if self._disk > CONST_DISK:
                    print("Internal Disk is full")
            if self.isWatchStopped:
                break

            time.sleep(TIMESLEEPTHREAD)

    def start(self):
        print("[]\tAGS Starting .....")
        try:
            if self.withCPU: 
                self.CPUThread = Thread(target=self.watchCPU, name="CPU")
                self.CPUThread.start()
            if self.withRAM: 
                self.RAMThread = Thread(target=self.watchRAM, name="RAM")
                self.RAMThread.start()
            if self.withDisk: 
                self.DiskThread = Thread(target=self.watchDisk, name="DISK")
                self.DiskThread.start()
        except KeyboardInterrupt or OSError:
            self.stop()

    def stop(self):
        self.isWatchStopped = True
        time.sleep(2)
        if self.CPUThread is not None: self.CPUThread.join()
        if self.RAMThread is not None: self.RAMThread.join()
        if self.DiskThread is not None: self.DiskThread.join()
        print("[]\tAGS Stopping .....")

if __name__=="__main__":
    ags = AGS(True, True, False, debug=False)
    
    ags.run()
    