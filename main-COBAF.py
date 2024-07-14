from camera1 import Cam1
from camera2 import Cam2
from constant import TIMESLEEPTHREAD
from yolo import YoloHandler
from ags import AGS
from constant import *

import argparse
import functools
import subprocess
import time
#import schedule
#from datetime import timedelta

class Main:
    
    def __init__(self, debug, withNCS=False, cpuFlag=True, ramFlag=True, diskFlag=True):
        if debug:
            self.camera1 = Cam1(debug=True)
            self.camera2 = Cam2(debug=True)
            self.yolo = YoloHandler(withNCS)
            self.ags = AGS(cpuFlag, ramFlag, diskFlag, debug=False)
           
        else:
            self.camera1 = Cam1(debug=False)
            self.camera2 = Cam2(debug=False)
            self.yolo = YoloHandler(withNCS)
            self.ags = AGS(cpuFlag, ramFlag, diskFlag, debug=False)
            
        self.runable = True
#        self.scheduling = True
        self.startTime = time.time()
        self.start()

    @functools.lru_cache(maxsize = None)
    def start(self):
        self.ags.start()

        self.yolo.start()
        
        self.camera1.setTimeToCapture(0)
        self.camera1.startCapture()
        
        self.camera2.setTimeToCapture(0)
        self.camera2.startCapture()
               
#        schedule.every(20).seconds.do(self.adaptCPURules)
#        schedule.every(1).minutes.do(self.adaptRAMRules)
#        schedule.every(3).minutes.do(self.adaptDiskRules)  
       
        try:
            while self.runable:
            
                self.camera1.stream()
                self.camera2.stream()
                
                self.yolo.setAgsTimeout(0)

#                if self.scheduling:
#                   schedule.run_pending()
#                   time.sleep(5)
#                if not self.scheduling:
#                   self.scheduling = True
                
                if time.time() - self.startTime > TIMEADAPTCPU:
                    self.adaptCPURules()
                elif time.time() - self.startTime > TIMEADAPTRAM:
                    self.adaptRAMRules()
                elif time.time() - self.startTime > TIMEADAPTDISK:
                    self.adaptDiskRules()                

                time.sleep(TIMESLEEPTHREAD)

#            self.RAMrestart()
        except KeyboardInterrupt or OSError:
            self.stop()
            
            
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
             self.scheduling = False
             print("cpu3 masuk")
        time.sleep(TIMESLEEPTHREAD)
        print("cpu masuk")
             
    def adaptRAMRules(self):
#        while self.ags._ram > CONST_RAM: 
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
             self.scheduling = False
             print("ram3 masuk")
         time.sleep(TIMESLEEPTHREAD)
         print("ram masuk")
           
    def adaptDiskRules(self):
#        while self.ags._disk > CONST_DISK: 
        if self.ags._disk > CONST_DISK and self.ags._disk < FULL_RESOURCE_DISK:
             self.camera1.setTimeToCapture(self.ags.getTimeToCapture())
             self.camera2.setTimeToCapture(self.ags.getTimeToCapture())
             print("disk1 masuk")
        elif self.ags._disk >= FULL_RESOURCE_DISK:
             self.ags.getDiskWarning()                    
             DiskClearing = subprocess.run(["sudo", "sh", "freeSpace.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
             print(DiskClearing.stdout)
             time.sleep(5)
             print("disk2 masuk")
        elif self.ags._disk < CONST_DISK:
             self.ags.DiskWarning = False
             self.ags.counterUpthDisk = 1
             self.scheduling = False
             print("disk3 masuk")
        time.sleep(TIMESLEEPTHREAD)   
        print("disk masuk")
                     
             
#    def adaptRules(self):
#        if self.ags._ram > CONST_RAM and self.ags._ram < FULL_RESOURCE or \
#            self.ags._cpu > CONST_CPU and self.ags._cpu < FULL_RESOURCE or \
#            self.ags._disk > CONST_DISK and self.ags._disk < FULL_RESOURCE_DISK:
#            
#                self.camera1.setTimeToCapture(self.ags.getTimeToCapture())
#                self.camera2.setTimeToCapture(self.ags.getTimeToCapture())
#                self.yolo.setAgsTimeout(self.ags.getTimeToProcess())
#                
#                print("1masuk sini gaaaaaaaaaaaaaa")
#        
#        elif self.ags._cpu >= FULL_RESOURCE or self.ags._ram >= FULL_RESOURCE or self.ags._disk >= FULL_RESOURCE_DISK:
#             if self.ags.getCPUWarning():
#                self.yolo.setAgsTimeout(10)

#             if self.ags.getRAMWarning():
#                self.runable = False

#             if self.ags.getDiskWarning():                    
#               DiskClearing = subprocess.run(["sudo", "sh", "freeSpace.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#               print(DiskClearing.stdout)
#               time.sleep(5)
#               
#             print("2masuk sini gaaaaaaaaaaaaaa")
#               
#        elif self.ags._cpu < CONST_CPU and self.ags._ram < CONST_RAM and self.ags._disk < CONST_DISK:
#             print(">>> Exit Scheduling..... <<<<")
#             self.scheduling = False
                  

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
    

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--debug", help="to debug with webcam", action="store_true")
    parser.add_argument("-c", "--cpu", help="to watch CPU avaibality", action="store_true")
    parser.add_argument("-r", "--ram", help="to watch RAM avaibality", action="store_true")
    parser.add_argument("-d", "--disk", help="to watch Internal Storage avaibality", action="store_true")
    
    args = parser.parse_args()
    
    Main(args.debug, args.cpu, args.ram, args.disk)


