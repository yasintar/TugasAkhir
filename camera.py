import cv2 as cv
from datetime import datetime
import threading

from constant import DEVICECAMERA, TIME

class Cam:
    def __init__(self) -> None:
        self.cap = cv.VideoCapture(DEVICECAMERA)
        self.frame = None

    def start(self):
        try:
            ret, self.frame = self.cap.read()
            if not ret:
                raise Exception('Camera Module not detected')
            cv.imshow('Stream', self.frame)
        except KeyboardInterrupt:
            print("Closing camera ...")
            self.stop()
        
    def stop(self):
        self.cap.release()
        cv.destroyAllWindows()

    def capture(self, tStop):
        self.captureThread()
        if not tStop.is_set():
            threading.Timer(TIME, self.capture, [tStop]).start()

    def captureThread(self):
        print("Capture")
        now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        name = "./images/{}.png".format(now)
        if self.frame is not None:
            if not cv.imwrite(name, self.frame):
                raise Exception('Could not write image')

if __name__ == "__main__":
    camera = Cam()
    while True:
        camera.start()