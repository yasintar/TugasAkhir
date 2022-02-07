import cv2 as cv

class Cam:
    def __init__(self) -> None:
        self.cap = cv.VideoCapture(0)
        self.run()

    def run(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                print('No Camera Module Detected')
                break

            cv.imshow('Stream', frame)
            k = cv.waitKey(5) & 0xFF
            if k == 27:
                break
        self.stop()

    def stop(self):
        self.cap.release()
        cv.destroyAllWindows()

if __name__ == "__main__":
    camera = Cam()