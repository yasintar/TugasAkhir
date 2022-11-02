from camera import Cam
from constant import TIMESLEEPTHREAD
from yolo import YoloHandler
from ags import AGS

import argparse
import functools
import subprocess
import time

class Main:
    def __init__(self, debug, withNCS=False, cpuFlag=True, ramFlag=True, diskFlag=True):
        if debug:
            self.camera = Cam(debug=True)
            self.yolo = YoloHandler(withNCS)
            self.ags = AGS(cpuFlag, ramFlag, diskFlag, debug=False)
            self.relay = None
        else:
            from relay import Relay
            self.camera = Cam(debug=False)
            self.yolo = YoloHandler(withNCS)
            self.ags = AGS(cpuFlag, ramFlag, diskFlag, debug=False)
            self.relay = Relay()

        self.runable = True
        self.isRelayOn = False
        self.start()

    @functools.lru_cache(maxsize = None)
    def start(self):
        self.ags.start()

        self.yolo.start()

        self.camera.setTimeToCapture(0)
        self.camera.startCapture()

        if self.relay is not None:
            self.relay.start()

        try:
            while self.runable:
                self.camera.stream()

                if self.ags.getCPUWarning():
                    print("[]\tAGS CPU Warning")

                if self.ags.getRAMWarning():
                    print("[]\tAGS CPU Warning")

                if self.ags.getDiskWarning():
                    print("[]\tAGS CPU Warning")

                if self.yolo.getYoloResult() is not None:
                    if self.yolo.getYoloResult()>0 and self.yolo.getYoloResult<2:
                        if self.relay is not None: self.relay.appendYoloRes(True)
                    elif self.yolo.getYoloResult()<=0:
                        if self.relay is not None: self.relay.appendYoloRes(False)

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
        self.camera.stop()
        if self.relay is not None: self.relay.stop()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--debug", help="to debug with webcam", action="store_true")
    parser.add_argument("-c", "--cpu", help="to watch CPU avaibality", action="store_true")
    parser.add_argument("-r", "--ram", help="to watch RAM avaibality", action="store_true")
    parser.add_argument("-d", "--disk", help="to watch Internal Storage avaibality", action="store_true")
    parser.add_argument("-n", "--ncs", help="work with Naural Computer Stick", action="store_true")
    args = parser.parse_args()
    Main(args.debug, args.ncs, args.cpu, args.ram, args.disk)