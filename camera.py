import cv2 as cv
from datetime import datetime
from threading import Thread
import os
import time

from constant import *

class Cam:
    def __init__(self, debug=True) -> None:
        self.isDebug = debug
        self.isStopped = False
        if debug: self.cap = cv.VideoCapture(DEVICEDEBUGCAMERA)
        else: 
            os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
            self.cap = cv.VideoCapture(DEVICESTGCAMERA, cv.CAP_FFMPEG)
        self.timeToCapture = None
        self.frame = None
        self.name = None
        self.captureThread = Thread(target=self.capture, name="CAPTURE")
        print("[]\tCAMERA Starting.....")

    def stream(self):
        ret, self.frame = self.cap.read()
        if not ret:
            print('[]\t(CAMERA) Camera Module not detected')
        else: cv.imshow('Stream', self.frame)

        c = cv.waitKey(5)
        if c == 27:
            self.stop()

    def startCapture(self):
        if not self.isStopped:
            self.captureThread.start()
        
    def stop(self):
        self.isStopped = True
        time.sleep(TIMESLEEPTHREAD)
        self.captureThread.join()
        self.cap.release()
        cv.destroyAllWindows()
        print("[]\tCAMERA Stopping .....")

    def setTimeToCapture(self, t):
        if t == 0:
            self.timeToCapture = TIME
        else:
            self.timeToCapture = t

    def getTimeToCapture(self):
        return self.timeToCapture

    def getImageName(self):
        return self.name

    def capture(self):
        if self.timeToCapture is not None:
            while True:
                now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
                self.name = "./image/{}.png".format(now)
                if self.frame is not None:
                    if not cv.imwrite(filename=self.name, img=self.frame):
                        self.stop()
                        raise Exception('[]\t(CAMERA) Could not write image')
                else:
                    print("[]\t(CAMERA) Frame not detected yet")
                
                if self.isStopped:
                    break

                time.sleep(self.timeToCapture)

if __name__ == "__main__":
    camera = Cam(False)
    while True:
        camera.stream()
        
