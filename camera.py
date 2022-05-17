import cv2 as cv
from datetime import datetime
import threading
import os

from constant import *

class Cam:
    def __init__(self, debug=True) -> None:
        if debug: self.cap = cv.VideoCapture(DEVICEDEBUGCAMERA)
        else: 
            os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
            self.cap = cv.VideoCapture(DEVICESTGCAMERA, cv.CAP_FFMPEG)
        self.frame = None

    def start(self):
        try:
            ret, self.frame = self.cap.read()
            if not ret:
                raise Exception('Camera Module not detected')
            # cv.imshow('Stream', self.frame)

            c = cv.waitKey(5)
            if c == 27:
                self.stop()
        except KeyboardInterrupt or OSError:
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
    flag = input()
    debug = None
    if flag == 'debug':
        debug = True
    else:
        debug = False
    camera = Cam(debug=debug)
    while True:
        camera.start()