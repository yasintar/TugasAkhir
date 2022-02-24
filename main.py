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
        while True:
            # print(threading.enumerate())

            self.camera.start()

            k = cv.waitKey(5) & 0xFF
            if k == 27:
                break
        self.camera.stop()

if __name__=="__main__":
    main = Main()