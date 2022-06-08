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
from constant import *

class AGS():
    def __init__(self, debug=True) -> None:
        self.RAMWarning = False
        if debug:
            self.timeToCapture = 1
            self._cpu = None
            self._ram = None
            self._disk = None
        else:
            self.timeToCapture = 1
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

    def setCurrentStat(self, cpu, ram, disk):
        self._cpu = cpu
        self._ram = ram
        self._disk = disk

    def watchCPU(self):
        tempCpuVal = 0
        while True:
            if self._cpu:
                if self._cpu > CONST_CPU:
                    if self._cpu > tempCpuVal:
                        self.timeToCapture = self.timeToCapture + 1
                        print("CPU Usage Exceed")
                else:
                    if self.timeToCapture > 1:
                        self.timeToCapture = self.timeToCapture - 1
                tempCpuVal = self._cpu

    def watchRAM(self):
        while True:
            if self._ram:
                if self._ram > CONST_RAM:
                    self.RAMWarning = True
                    print("RAM Usage Exceed")
                else:
                    self.RAMWarning = False

    def watchDisk(self):
        while True:
            if self._disk:
                if self._disk > CONST_DISK:
                    print("Internal Disk is full")

    def run(self):
        try:
            self.CPUThread = Thread(target=self.watchCPU, name="CPU")
            self.RAMThread = Thread(target=self.watchRAM, name="RAM")
            self.DiskThread = Thread(target=self.watchDisk, name="DISK")

            self.CPUThread.start()
            self.RAMThread.start()
            self.DiskThread.start()
        except KeyboardInterrupt or OSError:
            self.stop()

    def stop(self):
        self.CPUThread.join()
        self.RAMThread.join()
        self.RAMThread.join()

if __name__=="__main__":
    ags = AGS()

    # raw_input = input("format cpu,ram,disk :")
    # cpu, ram, disk = raw_input.split(',')
    # ags.setCurrentStat(int(cpu), int(ram), int(disk))

    # print("CPU Status: {}".format(ags.getCurrentCPUStat()))
    # print("RAM Stat: {}".format(ags.getCurrentRAMStat()))
    # print("Disk Stat: {}".format(ags.getCurrentDiskStat()))
    
    ags.run()
    