from constant import TIMESLEEPTHREAD
from integerDataReader import Reader
from ags import AGS

import argparse
import functools
import subprocess
import time

class Main:
    def __init__(self, debug, withCPU, withRAM, withDisk):
        self.dataReader = Reader("num.txt")
        self.ags = AGS(withCPU, withRAM, withDisk, False)
        if debug: self.relay = None
        else:
            from relay import Relay
            self.relay = Relay()

        self.runable = True
        self.isRelayOn = False
        self.start()

    @functools.lru_cache(maxsize = None)
    def start(self):
        self.dataReader.start()
        self.ags.start()
        if self.relay is not None:
            self.relay.start()

        try:
            while self.runable:
                if self.relay is not None:
                    if (int(self.dataReader.getNum())%3) == 1:
                        self.relay.appendYoloRes(True)
                    else:
                        self.relay.appendYoloRes(False)

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
        self.dataReader.stop()
        self.ags.stop()
        if self.relay is not None: self.relay.stop()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--debug", help="to debug with webcam", action="store_true")
    parser.add_argument("-c", "--cpu", help="to watch CPU avaibality", action="store_true")
    parser.add_argument("-r", "--ram", help="to watch RAM avaibality", action="store_true")
    parser.add_argument("-d", "--disk", help="to watch Internal Storage avaibality", action="store_true")
    args = parser.parse_args()
    Main(args.debug, args.cpu, args.ram, args.disk)