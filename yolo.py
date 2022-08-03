from threading import Thread
import cv2 as cv
import numpy as np
import time

from constant import *

class YOLO:
    def __init__(self, weight=YOLO_WEIGHT, cfg=YOLO_CFG, stream=False):
        self.stream = stream
        self.isStopped = False
        self.images = []
        self.result = None
        self.timeout = 0
        self.yoloThread = Thread(target=self.run, name="YOLO")
        self.net = cv.dnn.readNet(weight,cfg)
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)

    def detect(self, image):
        try:
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
                        
            self.result = self.confiAvg(confidences)
        except Exception as e:
            print(str(e))
            self.result = 0
        finally:
            print("[]\t(YOLO) detect result : "+str(self.result))

    def confiAvg(self, confidences):
        if len(confidences) != 0:
            return sum(confidences)/len(confidences)
        return 0

    def prepareImg(self, image):
        if not self.stream:
            image = cv.imread(image)
        blob = cv.dnn.blobFromImage(image, YOLO_SCALE, YOLO_IMGSIZE, (0,0,0), True, crop=False)
        self.net.setInput(blob)

    def getYoloResult(self):
        return self.result

    def setTimeout(self, time):
        self.timeout = time

    def appendImage(self, image):
        self.images.append(image)

    def run(self):
        while True:
            if self.images != []:
                self.result = self.detect(self.images[0])
                self.images.pop(0)

                t_end = time.time() + self.timeout
                while time.time() < t_end:
                    if self.images != []:
                        self.images.pop(0)
            
            if self.isStopped:
                break

            time.sleep(TIMESLEEPTHREAD)

    def start(self):
        print("[]\tYOLO Starting .....")
        self.yoloThread.start()

    def stop(self):
        print("[]\tYOLO Stopping .....")
        self.isStopped = True
        time.sleep(TIMESLEEPTHREAD)
        self.yoloThread.join()
    
if __name__=="__main__":
    detector = YOLO()
    detector.detect("./image/coba.jpg")
    print(detector.getYoloResult())