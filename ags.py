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

CONST_CPU = 50      #Batas usage CPU jika lebih do something
CONST_RAM = 80      #Batas usage RAM jika lebih do something
CONST_DISK = 80     #Batas usage Disk jika lebih do something


import psutil
import time
from threading import Thread

class AGS(Thread):
    def __init__(self, debug=False) -> None:

        if not debug:
            Thread.__init__(self)

        self.timeInterval = 1
        self._cpu = psutil.cpu_percent(0.1)
        self._ram = psutil.virtual_memory()[2]
        self._disk = psutil.disk_usage('/')[3]

    def getCurrentCPUStat(self):
        return self._cpu

    def getCurrentRAMStat(self):
        return self._ram

    def getCurrentDiskStat(self):
        return self._disk

    def watchCPU(self):
        if self._cpu > CONST_CPU:
            print("CPU Usage Exceed")
        print("CPU Normal Usage")
        
    def watchRAM(self):
        if self._ram > CONST_RAM:
            print("RAM Usage Exceed")
        print("RAM Normal Usage")

    def watchDisk(self):
        if self._disk > CONST_DISK:
            print("Internal Disk is full")
        print("Internal Disk is safe")

    def evaluate(self):
        pass


if __name__=="__main__":
    ags = AGS()

    while True:
        print("CPU Status: {}".format(ags.getCurrentCPUStat()))
        print("RAM Stat: {}".format(ags.getCurrentRAMStat()))
        print("Disk Stat: {}".format(ags.getCurrentDiskStat()))
        time.sleep(10)
    