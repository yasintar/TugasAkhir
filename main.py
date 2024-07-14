from camera1 import Cam1
from camera2 import Cam2
from constant import TIMESLEEPTHREAD
from yolo import YoloHandler
from ags import AGS
from constant import *
from schedule import Schedule 

import argparse
import functools
import subprocess
import time
import sched

class Main:
    
    def __init__(self, debug, withNCS=False, cpuFlag=True, ramFlag=True, diskFlag=True):
        if debug:
            self.camera1 = Cam1(debug=True)
            self.camera2 = Cam2(debug=True)
            self.yolo = YoloHandler(withNCS)
            self.ags = AGS(cpuFlag, ramFlag, diskFlag, debug=False)
            self.schedule = Schedule(self.camera1, self.camera2, self.yolo, self.ags)
           
        else:
            self.camera1 = Cam1(debug=False)
            self.camera2 = Cam2(debug=False)
            self.yolo = YoloHandler(withNCS)
            self.ags = AGS(cpuFlag, ramFlag, diskFlag, debug=False)
            self.schedule = Schedule(self.camera1, self.camera2, self.yolo, self.ags)
            
        self.runable = True
        self.start()

    @functools.lru_cache(maxsize = None)
    def start(self):
        self.ags.start()

        self.yolo.start()
        
        self.schedule.adaptCPU_repeat()
        self.schedule.adaptRAM_repeat()
        self.schedule.adaptDisk_repeat()
        self.schedule.startSchedule()      
        
        self.camera1.setTimeToCapture(0)
        self.camera1.startCapture()
        
        self.camera2.setTimeToCapture(0)
        self.camera2.startCapture()
       
        try:
            while self.runable:
            
                self.camera1.stream()
                self.camera2.stream()
                
                self.yolo.setAgsTimeout(0)
                                
                if self.ags.getCPUWarning():
                    self.yolo.setAgsTimeout(10)
                    print("cpu2 masuk by main")

                if self.ags.getRAMWarning():
                    self.runable = False
                    print("ram2 masuk by main")

                if self.ags.getDiskWarning():                    
                    DiskClearing = subprocess.run(["sudo", "sh", "freeSpace.sh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                    print(DiskClearing.stdout)
                    time.sleep(5)
                    print("disk2 masuk by main")
                                               
                time.sleep(TIMESLEEPTHREAD)

            self.RAMrestart()
        except KeyboardInterrupt or OSError:
            self.stop()                  

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
        self.schedule.stop()
        
    

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--debug", help="to debug with webcam", action="store_true")
    parser.add_argument("-c", "--cpu", help="to watch CPU avaibality", action="store_true")
    parser.add_argument("-r", "--ram", help="to watch RAM avaibality", action="store_true")
    parser.add_argument("-d", "--disk", help="to watch Internal Storage avaibality", action="store_true")
    
    args = parser.parse_args()
    
    Main(args.debug, args.cpu, args.ram, args.disk)


