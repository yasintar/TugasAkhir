from camera import Cam
import cv2 as cv

class Main:
    def __init__(self) -> None:
        self.camera = Cam()
        self.run()

    def run(self):
        while True:
            self.camera.start()

            self.camera.capture()

            k = cv.waitKey(5) & 0xFF
            if k == 27:
                break
        self.camera.stop()

if __name__=="__main__":
    main = Main()