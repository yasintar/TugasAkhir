import watchdog.events
import watchdog.observers
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

class EventHandler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        self.yoloDetector = YOLO()
        self.yoloRes = None
        self.isNewFileDetected = False
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.png'],
                                                             ignore_directories=True, case_sensitive=False)
  
    def on_created(self, event):
        print("Watchdog received created event - % s." % event.src_path)
        result = self.yoloDetector.detect(event.src_path)
        self.setYoloResult(result)
        print("YOLO Res : ", self.getYoloResult())

    def setYoloResult(self, result):
        self.yoloRes = result

    def getYoloResult(self):
        return self.yoloRes

class YoloHandler:
    def __init__(self):
        self.event_handler = EventHandler()
        self.observer = watchdog.observers.Observer()

    def start(self):
        self.observer.schedule(self.event_handler, path=IMG_PATH, recursive=True)
        self.observer.start()
        try:
            while True:
                pass
        except KeyboardInterrupt or OSError:
            self.stop()

    def stop(self):
        self.observer.stop()
        self.observer.join()

    def getYoloResult(self):
        return self.event_handler.getYoloResult()

if __name__=="__main__":
    detector = YoloHandler()
    detector.start()