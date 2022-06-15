import cv2 as cv
from datetime import datetime
from threading import Thread, Timer
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
        self.captureThread = Thread(target=self.capture, name="CAPTURE")
        print("[]\tCAMERA Starting.....")

    def start(self):
        try:
            ret, self.frame = self.cap.read()
            if not ret:
                raise Exception('Camera Module not detected')
            if self.isDebug: cv.imshow('Stream', self.frame)

            c = cv.waitKey(5)
            if c == 27:
                self.stop()
        except KeyboardInterrupt or OSError:
            print("Closing camera ...")
            self.stop()
        
    def stop(self):
        self.isStopped = True
        time.sleep(2)
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

    def capture(self):
        if self.timeToCapture is not None:
            while True:
                # self.captureThread = threading.Timer(self.timeToCapture, self.capture).start()
                # print("Capture")
                now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
                name = "./image/{}.png".format(now)
                if self.frame is not None:
                    if not cv.imwrite(filename=name, img=self.frame):
                        self.stop()
                        raise Exception('Could not write image')
                else:
                    print("Frame not detected yet")
                time.sleep(self.timeToCapture)
                if self.isStopped:
                    break

if __name__ == "__main__":
    flag = input()
    debug = None
    if flag == 'debug':
        debug = True
    else:
        debug = False
    camera = Cam(debug=debug)
    camera.setTimeToCapture(5)
    camera.capture()
    while True:
        camera.start()
        n = input()
        if n == 'n':
            camera.stop()
