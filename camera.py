import cv2 as cv

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

if __name__ == "__main__":
    camera = Cam()