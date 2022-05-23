from camera import Cam
import cv2 as cv
import threading

class Main:
    def __init__(self) -> None:
        self.camera = Cam()
        self.run()

    def run(self):
        tStop = threading.Event()
        self.camera.capture(tStop)
        try:
            while True:

                self.camera.start()
        except IOError or OSError or KeyboardInterrupt:
            self.camera.stop()
        finally:
            print("System Stopped")

if __name__=="__main__":
    main = Main()