from camera1 import Cam1
from camera2 import Cam2
from constant import TIMESLEEPTHREAD
from yolo import YoloHandler
from ags import AGS
from constant import *
from threading import Thread
import sched
import time
import threading

class Schedule:
    def __init__(self, camera1, camera2, yolo, ags):
        self.yolo = yolo
        self.ags = ags
        self.camera1 = camera1
        self.camera2 = camera2

        self.isStopped = False
        
        self.scheduler = sched.scheduler(time.time, time.sleep)
#        self.scheduler.enter(10, 1, self.adaptCPURules)
#        self.scheduler.enter(20, 1, self.adaptRAMRules)
#        self.scheduler.enter(60, 1, self.adaptDiskRules)
        
#        self.scheduleThread = Thread(target=self.scheduler.run, name="SCHEDULE")
        self.scheduleThread = Thread(target=self.start_adapt_all, name="SCHEDULE")
#       threading.Thread(target=self.scheduler.run).start()
        print("[]\tScheduler starting.....")
        
        
    def start_adapt_all(self):
        while not self.isStopped:
            self.scheduler.run()
            time.sleep(1)            
    
    def adaptCPU_repeat(self):
        if not self.isStopped:
            self.scheduler.enter(5,1, self.adaptCPURules)
            self.scheduler.enter(5,1, self.adaptCPU_repeat)
#        if self.isStopped: self.stop()
        
    def adaptRAM_repeat(self):
        if not self.isStopped:
            self.scheduler.enter(15,1, self.adaptRAMRules)
            self.scheduler.enter(15,1, self.adaptRAM_repeat)
#        if self.isStopped: self.stop()
    
    def adaptDisk_repeat(self):
        if not self.isStopped:
            self.scheduler.enter(60,1, self.adaptDiskRules)
            self.scheduler.enter(60,1, self.adaptDisk_repeat)
#        if self.isStopped: self.stop()
        
#    def adaptPasstoMain(self):
#        if not self.isStopped:
#            self.scheduler.enter(5,1, self.adaptCPURules)
#            self.scheduler.enter(10,1, self.adaptRAMRules)
#            self.scheduler.enter(60,1, self.adaptDiskRules)
#        if self.isStopped: self.stop()
        
    def startSchedule(self):
        if not self.isStopped:
            self.scheduleThread.start()
            
    def stop(self):
        self.isStopped = True
        time.sleep(3)
        self.scheduleThread.join()
        print("[]\tScheduler is stopped.....")
        
             
    def adaptCPURules(self):
        if self.ags._cpu > CONST_CPU and self.ags._cpu < FULL_RESOURCE:
            self.yolo.setAgsTimeout(self.ags.getTimeToProcess())
            print("cpu1 masuk")
        elif self.ags._cpu >= FULL_RESOURCE:
            self.ags.getCPUWarning()
            print("cpu2 masuk")
        elif self.ags._cpu < CONST_CPU:
            self.ags.CPUWarning = False
            self.ags.counterUpthCPU = 1
            print("cpu3 masuk")
        time.sleep(TIMESLEEPTHREAD)
        print("cpu masuk")

        
    def adaptRAMRules(self):
        if self.ags._ram > CONST_RAM and self.ags._ram < FULL_RESOURCE:
            self.camera1.setTimeToCapture(self.ags.getTimeToCapture())
            self.camera2.setTimeToCapture(self.ags.getTimeToCapture())
            time.sleep(1)
            print("ram1 masuk")
        elif self.ags._ram >= FULL_RESOURCE:
            self.ags.getRAMWarning()
            print("ram2 masuk")
        elif self.ags._ram < CONST_RAM:
            self.ags.RAMWarning = False
            self.ags.counterUpthRAM = 1
            print("ram3 masuk")
        time.sleep(TIMESLEEPTHREAD)
        print("ram masuk")

        
    def adaptDiskRules(self):
        if self.ags._disk > CONST_DISK and self.ags._disk < FULL_RESOURCE_DISK:
            self.camera1.setTimeToCapture(self.ags.getTimeToCapture())
            self.camera2.setTimeToCapture(self.ags.getTimeToCapture())
            print("disk1 masuk")
        elif self.ags._disk >= FULL_RESOURCE_DISK:
            self.ags.getDiskWarning()       
            print("disk2 masuk")
        elif self.ags._disk < CONST_DISK:
            self.ags.DiskWarning = False
            self.ags.counterUpthDisk = 1
            print("disk3 masuk")
        time.sleep(TIMESLEEPTHREAD)
        print("disk masuk")
        

        
if __name__ == "__main__":
    schedule = Schedule()
    try:
        schedule.start()
    except KeyboardInterrupt:
        schedule.stop()
    finally:
        exit()

