import cv2 as cv
from constant import *

class YOLO:
    def __init__(self, weight, cfg):
        self.net = cv.dnn.readNet(weight,cfg)

    def detect(self, image):
        self.prepareImg(image=image)
        

    def prepareImg(self, image):
        blob = cv.dnn.blobFromImage(image, YOLO_SCALE, YOLO_IMGSIZE, (0,0,0), True, crop=False)
        self.net.setInput(blob)

if __name__=="__main__":
    detector = YOLO("./model/yolo-obj_last.weights","./model/yolo-obj.cfg")
    if detector: print("success")