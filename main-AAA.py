from camera1 import Cam1
from camera2 import Cam2
from constant import TIMESLEEPTHREAD
from yolo import YoloHandler
from ags import AGS
from constant import *
#from schedule import Schedule 

import argparse
import functools
import subprocess
import time
import sched
import threading

class Main:
    
    def __init__(self, debug, withNCS=False, cpuFlag=True, ramFlag=True, diskFlag=True):
        if debug:
            self.camera1 = Cam1(debug=True)
            self.camera2 = Cam2(debug=True)
            self.yolo = YoloHandler(withNCS)
            self.ags = AGS(cpuFlag, ramFlag, diskFlag, debug=False)
#            self.schedule = Schedule(debug=True)
           
        else:
            self.camera1 = Cam1(debug=False)
            self.camera2 = Cam2(debug=False)
            self.yolo = YoloHandler(withNCS)
            self.ags = AGS(cpuFlag, ramFlag, diskFlag, debug=False)
#            self.schedule = Schedule(debug=False)
            
        self.runable = True
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.start()

    @functools.lru_cache(maxsize = None)
    def start(self):
        self.ags.start()

        self.yolo.start()
        
        self.camera1.setTimeToCapture(0)
        self.camera1.startCapture()
        
        self.camera2.setTimeToCapture(0)
        self.camera2.startCapture()
                
#        self.schedule.startSchedule()
        threading.Thread(target=self.scheduler.run).start()
        self.adaptCPU_repeat()
        self.adaptRAM_repeat()
        self.adaptDisk_repeat() 
       
        try:
            while self.runable:
            
                self.camera1.stream()
                self.camera2.stream()
                                                               
                self.yolo.setAgsTimeout(0)
                self.scheduler.run()                                      
                                               
                time.sleep(TIMESLEEPTHREAD)

            self.RAMrestart()
        except KeyboardInterrupt or OSError:
            self.stop()
            
#    def start_adapt_all(self):
#        self.adaptCPU_repeat()
#        self.adaptRAM_repeat()
#        self.adaptDisk_repeat()
#        self.scheduler.run()
    
    def adaptCPU_repeat(self):
        self.scheduler.enter(10,1, self.adaptCPURules)
        self.scheduler.enter(10,1, self.adaptCPU_repeat)
        
    def adaptRAM_repeat(self):
        self.scheduler.enter(20,1, self.adaptRAMRules)
        self.scheduler.enter(20,1, self.adaptRAM_repeat)
    
    def adaptDisk_repeat(self):
        self.scheduler.enter(60,1, self.adaptDiskRules)
        self.scheduler.enter(60,1, self.adaptDisk_repeat)        
             
    def adaptCPURules(self):
        if self.ags._cpu > CONST_CPU and self.ags._cpu < FULL_RESOURCE:
            self.yolo.setAgsTimeout(self.ags.getTimeToProcess())
            print("cpu1 masuk")
        elif self.ags._cpu >= FULL_RESOURCE:
            self.ags.getCPUWarning()
            self.yolo.setAgsTimeout(10)
            print("cpu2 masuk")
        elif self.ags._cpu < CONST_CPU:
            self.ags.CPUWarning = False
            self.ags.counterUpthCPU = 1
            print("cpu3 masuk")
        time.sleep(TIMESLEEPTHREAD)
        print("cpu masuk")
#        self.scheduler.enter(10, 1, self.adaptCPURules)
        
    def adaptRAMRules(self):
        if self.ags._ram > CONST_RAM and self.ags._ram < FULL_RESOURCE:
            self.camera1.setTimeToCapture(self.ags.getTimeToCapture())
            self.camera2.setTimeToCapture(self.ags.getTimeToCapture())
            time.sleep(1)
            print("ram1 masuk")
        elif self.ags._ram >= FULL_RESOURCE:
            self.ags.getRAMWarning()
            self.runable = False
            self.RAMrestart()
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
            print("Running Disk Clearing Script")
            time.sleep(5)
            print("disk2 masuk")
        elif self.ags._disk < CONST_DISK:
            self.ags.DiskWarning = False
            self.ags.counterUpthDisk = 1
            print("disk3 masuk")
        time.sleep(TIMESLEEPTHREAD)
        print("disk masuk")        
                      

    def RAMrestart(self):
        if not self.runable:
            self.stop()
            self.runable = True
            self.start.cache_clear()
            RAMClearing = subprocess.run(["sudo", "sh", "freeRAM.sh"], stdout=subprocess.PIPE,stderr=subprocess.PIPE, text=True)
            print(RAMClearing.stdout)
            self.start()

    def stop(self):
        self.ags.stop()
        self.yolo.stop()
        self.camera1.stop()
        self.camera2.stop()
#        self.schedule.stop()
    

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--debug", help="to debug with webcam", action="store_true")
    parser.add_argument("-c", "--cpu", help="to watch CPU avaibality", action="store_true")
    parser.add_argument("-r", "--ram", help="to watch RAM avaibality", action="store_true")
    parser.add_argument("-d", "--disk", help="to watch Internal Storage avaibality", action="store_true")
    
    args = parser.parse_args()
    
    Main(args.debug, args.cpu, args.ram, args.disk)


