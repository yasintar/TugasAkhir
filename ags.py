import psutil
from threading import Thread
import time
from datetime import datetime
import pandas as pd
from constant import *

class AGS():
    def __init__(self, withCPU, withRAM, withDisk, debug=True) -> None:
        self.withCPU = withCPU
        self.withRAM = withRAM
        self.withDisk = withDisk

        self.CPUThread = None
        self.RAMThread = None
        self.DiskThread = None

        self.CPUData = []
        self.RAMData = []
        self.DiskData = []

        self.RAMWarning = False
        self.CPUWarning = False
        self.DiskWarning = False

        self.isWatchStopped = False

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

    def getDiskWarning(self):
        return self.DiskWarning

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
        CPUStartTime = time.time()
        while True:
            self._cpu = psutil.cpu_percent(0.1)
            if self._cpu:
                CPUTemp = None
                if self._cpu >= FULL_RESOURCE:
                    self.CPUWarning = True
                CPUTemp = [datetime.now().strftime("%H:%M:%S"), time.time()-CPUStartTime, self._cpu]
                self.CPUData.append(CPUTemp)

            if self.isWatchStopped:
                break

            time.sleep(TIMESLEEPTHREAD)

    def watchRAM(self):
        print("[]\t(AGS) Watching RAM")
        RAMStartTime = time.time()
        while True:
            self._ram = psutil.virtual_memory()[2]
            if self._ram:
                RAMTemp = None
                if self._ram >= FULL_RESOURCE:
                    self.RAMWarning = True
                RAMTemp = [datetime.now().strftime("%H:%M:%S"), time.time()-RAMStartTime, self._ram]
                self.RAMData.append(RAMTemp)

            if self.isWatchStopped:
                break

            time.sleep(TIMESLEEPTHREAD)

    def watchDisk(self):
        print("[]\t(AGS) Watching Disk Space")
        DiskStartTime = time.time()
        while True:
            self._disk = psutil.disk_usage('/')[3]
            if self._disk:
                DiskTemp = None
                if self._disk >= FULL_RESOURCE:
                    self.DiskWarning = True
                DiskTemp = [datetime.now().strftime("%H:%M:%S"), time.time()-DiskStartTime, self._disk]
                self.DiskData.append(DiskTemp)

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
        time.sleep(TIMESLEEPTHREAD)
        if self.CPUThread is not None: self.CPUThread.join()
        if self.RAMThread is not None: self.RAMThread.join()
        if self.DiskThread is not None: self.DiskThread.join()

        CPUdf = pd.DataFrame(self.CPUData, columns=['Time', 'Time_Elapsed', 'CPU_Precentage'])
        CPUdf.to_csv('./dataLog/CPU.csv', index=True)

        RAMdf = pd.DataFrame(self.RAMData, columns=['Time', 'Time_Elapsed', 'RAM_Precentage'])
        RAMdf.to_csv('./dataLog/RAM.csv', index=True)

        Diskdf = pd.DataFrame(self.DiskData, columns=['Time', 'Time_Elapsed', 'Disk_Precentage'])
        Diskdf.to_csv('./dataLog/Disk.csv', index=True)
        print("[]\tAGS Stopping .....")

if __name__=="__main__":
    ags = AGS(True, True, False, debug=False)
    
    try:
        ags.start()
    except KeyboardInterrupt:
        ags.stop()
    finally:
        exit()
    
