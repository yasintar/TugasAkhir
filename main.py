from camera import Cam
from yolo import YoloHandler
from ags import AGS
from relay import Relay
import functools

class Main:
    def __init__(self) -> None:
        self.camera = Cam(debug=True)
        self.yolodetector = YoloHandler()
        self.ags = AGS(debug=False)
        self.relay = Relay()

        self.runable = True
        self.isDetected = 0
        self.run()

    @functools.lru_cache(maxsize = None)
    def run(self):
        self.ags.run()

        self.yolodetector.start()

        self.camera.setTimeToCapture(0)
        self.camera.captureThread.start()
        
        try:
            while self.runable:
                self.camera.start()
                self.camera.setTimeToCapture(self.ags.timeToCapture)

                if self.ags.getRAMWarning():
                    self.runable = False

                if self.yolodetector.getYoloResult() is not None:
                    self.isDetected = 1
                    
            self.restart()
        except KeyboardInterrupt or OSError:
            self.stop()

    def restart(self):
        if not self.runable:
            self.stop()
            self.runable = True
            self.ags.run()
            self.run.cache_clear()
            self.run()

    def stop(self):
        self.ags.stop()
        self.camera.stop()
        self.yolodetector.stop()

if __name__=="__main__":
    main = Main()