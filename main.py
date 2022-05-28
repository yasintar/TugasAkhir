from camera import Cam
from yolo import YOLO
from ags import AGS
from relay import Relay
import functools

class Main:
    def __init__(self) -> None:
        self.camera = Cam(debug=True)
        self.yolodetector = YOLO()
        self.ags = AGS(debug=False)
        self.relay = Relay()
        self.runable = True
        self.run()

    @functools.lru_cache(maxsize = None)
    def run(self):
        self.ags.start()

        self.camera.setTimeToCapture(0)
        self.camera.captureThread.start()
        
        while self.runable:
            self.camera.start()
            self.camera.setTimeToCapture(self.ags.timeToCapture)

            if self.ags.getRAMWarning():
                self.restart()

    def restart(self):
        if self.runable:
            self.ags.stop()
            self.ags.join()
            self.camera.stop()

            self.runable = False
            self.ags = AGS(debug=False)
            self.run.cache_clear()
            self.run()

if __name__=="__main__":
    main = Main()