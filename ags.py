"""
Algorithm Granularity Settings

Pengaturan yang dilakukan untuk dapat memaksimalkan kinerja program
untuk data stream mining supaya resource komputer tidak cepat penuh

Program ini mengatur Resource berikut
1. CPU

Apabila Konsumsi CPU -> TINGGI, Waktu penangkapan gambar dikurangi

2. RAM

Apabila RAM telah terkonsumsi tinggi, cache dikurangi

3. Disk

Apabila Disk penuh, latest image dihapus, dan hanya mengambil
ketika terjadi sebuah event
"""
import psutil
from threading import Thread
import time
from random import randint
from constant import *

class AGS():
    def __init__(self, debug=True) -> None:
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

    def setCurrentStat(self, cpu, ram, disk):
        self._cpu = cpu
        self._ram = ram
        self._disk = disk

    def watchCPU(self):
        print("Watching CPU")
        while True:
            if self._cpu:
                if self._cpu > CONST_CPU and self._cpu < FULL_RESOURCE:
                    self.timeToProcess = randint(1,5)*self.counterUpthCPU
                    self.counterUpthCPU = self.counterUpthCPU + 1
                elif self._cpu >= FULL_RESOURCE:
                    self.CPUWarning = True
                elif self._cpu < CONST_CPU:
                    self.counterUpthCPU = 1
            
            if self.isWatchStopped:
                break

    def watchRAM(self):
        print("Watching RAM")
        while True:
            if self._ram:
                if self._ram > CONST_RAM and self._ram < FULL_RESOURCE:
                    if self.RAMWarning : self.RAMWarning = False
                    self.timeToCapture = 1 + (1 - (CONST_RAM/100)) * self.counterUpthRAM
                elif self._ram >= FULL_RESOURCE:
                    self.RAMWarning = True
                elif self._ram < CONST_RAM:
                    self.counterUpthRAM = 1
                    self.RAMWarning = False

            if self.isWatchStopped:
                break

    def watchDisk(self):
        print("Watching Disk")
        while True:
            if self._disk:
                if self._disk > CONST_DISK:
                    print("Internal Disk is full")
                else:
                    print('Disk is Safe '+str(self._disk))
            if self.isWatchStopped:
                break

    def run(self):
        print("[]\tAGS Starting .....")
        try:
            self.CPUThread = Thread(target=self.watchCPU, name="CPU")
            self.RAMThread = Thread(target=self.watchRAM, name="RAM")
            # self.DiskThread = Thread(target=self.watchDisk, name="DISK")

            self.CPUThread.start()
            self.RAMThread.start()
            # self.DiskThread.start()
        except KeyboardInterrupt or OSError:
            self.stop()

    def stop(self):
        self.isWatchStopped = True
        time.sleep(2)
        self.CPUThread.join()
        self.RAMThread.join()
        # self.DiskThread.join()
        print("[]\tAGS Stopping .....")

if __name__=="__main__":
    ags = AGS(debug=False)
    
    ags.run()
    