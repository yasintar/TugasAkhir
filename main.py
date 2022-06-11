from ast import arg
from camera import Cam
from yolo import YoloHandler
from ags import AGS
from relay import Relay

import argparse
import functools

class Main:
    def __init__(self, debug) -> None:
        if debug:
            self.camera = Cam(debug=True)
            self.yolodetector = YoloHandler()
            self.ags = AGS(debug=False)
            self.relay = None
        else:
            self.camera = Cam(debug=False)
            self.yolodetector = YoloHandler()
            self.ags = AGS(debug=False)
            self.relay = Relay()

        self.runable = True
        self.isRelayOn = False
        self.start()

    @functools.lru_cache(maxsize = None)
    def start(self):
        self.ags.run()

        self.yolodetector.start()

        self.camera.setTimeToCapture(0)
        self.camera.captureThread.start()

        if self.relay is not None:
            self.relay.start()
        
        try:
            while self.runable:
                self.camera.start()
                self.camera.setTimeToCapture(self.ags.timeToCapture)

                if self.ags.getRAMWarning():
                    self.runable = False

                if self.yolodetector.getYoloResult() is not None:
                    self.relay.appendYoloRes(True)
                else:
                    self.relay.appendYoloRes(False)
                    
            self.restart()
        except KeyboardInterrupt or OSError:
            self.stop()

    def restart(self):
        if not self.runable:
            self.stop()
            self.runable = True
            self.start.cache_clear()
            self.start()

    def stop(self):
        self.ags.stop()
        self.yolodetector.stop()
        self.camera.stop()
        self.yolodetector.stop()
        if self.relay is not None: self.relay.stop()

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="to debug with webcam")
    main = Main()