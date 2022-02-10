from logging import exception
import cv2 as cv
from datetime import datetime
import os

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
        now = datetime.now().strftime("%d_%m_%Y-%H:%M:%S")
        name = "./images/{}.png".format(now)
        if self.frame is not None:
            if not cv.imwrite(name, self.frame):
                raise Exception('Could not write image')

    def showImg(self):
        path = os.path.join(os.getcwd(), 'images', 'Screenshot from 2022-01-12 16-10-15.png')
        while True:
            img = cv.imread(path)

            cv.imshow('img', img)

if __name__ == "__main__":
    camera = Cam()
    camera.showImg()