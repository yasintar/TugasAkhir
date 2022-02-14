from logging import exception
import cv2 as cv
from datetime import datetime

class Cam:
    def __init__(self) -> None:
        self.cap = cv.VideoCapture(0)
        self.frame = None

    def start(self):
        ret, self.frame = self.cap.read()
        if not ret:
            print('Camera Module not Connected')
        cv.imshow('Stream', self.frame)

    def stop(self):
        self.cap.release()
        cv.destroyAllWindows()

    def capture(self):
        print("Capture")
        now = datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        name = "./images/{}.png".format(now)
        if self.frame is not None:
            if not cv.imwrite(name, self.frame):
                raise Exception('Could not write image')

if __name__ == "__main__":
    camera = Cam()