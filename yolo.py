import cv2 as cv
import numpy as np

from constant import *

class YOLO:
    def __init__(self, weight=YOLO_WEIGHT, cfg=YOLO_CFG):
        self.net = cv.dnn.readNet(weight,cfg)

    def detect(self, image):
        self.prepareImg(image=image)
        layer_names = self.net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        confidences = []
        class_ids = []

        outs = self.net.forward(output_layers)
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]

                if confidence > YOLO_CONFI:
                    class_ids.append(class_id)
                    confidences.append(confidence)
                    
        return self.confiAvg(confidences)

    def confiAvg(self, confidences):
        return sum(confidences)/len(confidences)

    def prepareImg(self, image):
        image = cv.imread(image)
        blob = cv.dnn.blobFromImage(image, YOLO_SCALE, YOLO_IMGSIZE, (0,0,0), True, crop=False)
        self.net.setInput(blob)

if __name__=="__main__":
    detector = YOLO("./model/yolo-obj_last.weights","./model/yolo-obj.cfg")
    detector.detect("./image/coba.jpg")
    if detector: print("success")