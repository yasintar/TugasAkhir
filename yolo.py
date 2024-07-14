from threading import Thread
from datetime import datetime

import torch.hub
import watchdog.events
import watchdog.observers
import pandas as pd
import cv2 as cv
import numpy as np
import time

from constant import *

class YOLO:
    def __init__(self, withNCS, weight=YOLO_WEIGHT, cfg=YOLO_CFG, stream=False):
        self.stream = stream
        self.images = []
        self.result = 0
        self.timeout = None
        self.resumeTime = None
        self.net = torch.hub.load('WongKinYiu/yolov7', 'custom', 'model/yolov7-tiny.pt', trust_repo=True, force_reload=False)
        self.net.conf = YOLO_CONFI
        self.net.eval()
       # if withNCS: self.net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)

    def detect(self, image):
        if not self.isContinueProcess():
            return 2
        elif self.isContinueProcess():
            self.timeout = None
            self.resumeTime = None
            try:
                self.prepareImg(image=image)
                outs = self.net(image, size=416)
                #print(image)
            
                #outs.print()
                result = outs.pandas().xyxy[0]
                #print(result)
                confidences = result['confidence'].values.tolist()
                class_ids = result['class'].values.tolist()
                #print(confidences)
                #print(class_ids)
                
                #print("lewat 1")
                avg = self.confiAvg(confidences)
                
                #print("lewat 2")
                analyzefile = pd.DataFrame({
                    'timeProcessed': [datetime.now().strftime("%d-%m-%Y_%H:%M:%S")],
                    'filename': [image],
                    'score': [avg],
                    'detect': [len(class_ids)]
                })
                analyzefile.to_csv('./dataLog/YOLODetectLog.csv', mode='a', index=False, header=False)
                            
                return avg
            except Exception as e:
                print(str(e))
                return 0

    def confiAvg(self, confidences):
        if len(confidences) != 0:
            return sum(confidences)/len(confidences)
        return 0

    def prepareImg(self, image):
        if not self.stream:
            image = cv.imread(image)
        if image is None:
            print('[]\tYOLO image not read correctly')

    def isContinueProcess(self):
        if self.resumeTime is not None:
            now = datetime.now()
            diff = now - self.resumeTime
            diff = diff.total_seconds()
            if diff >= self.timeout:
                return True
        return False

    def setTimeoutYOLO(self, num):
        if self.resumeTime is None:
            self.resumeTime = datetime.now()
            self.timeout = num
            print("[]\tYOLO process delay for {} s".format(num))

class EventHandler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self, withNCS):
        self.yoloDetector = YOLO(withNCS)
        self.yoloRes = None
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.jpg'],
                                                             ignore_directories=True, case_sensitive=False)
  
    def on_created(self, event):
        time.sleep(TIMESLEEPTHREAD)
        result = self.yoloDetector.detect("./"+str(event.src_path[2:]))
        self.setYoloResult(result)
        print("[]\tYOLO Res in "+str(event.src_path[2:])+" : ", self.getYoloResult())

    def setYoloResult(self, result):
        self.yoloRes = result

    def getYoloResult(self):
        return self.yoloRes

    def setTimeoutYOLO(self, num):
        self.yoloDetector.setTimeoutYOLO(num)

class YoloHandler(watchdog.observers.Observer):
    def __init__(self, withNCS):
        print("[]\tYOLO Starting.....")
        self.isStopped = False
        self.timeoutWatchdog = 0
        self.event_handler = EventHandler(withNCS)
        self.observer = watchdog.observers.Observer()
        self.handlerThread = Thread(target=self.run, name="YoloHandler")

    def setAgsTimeout(self, num):
        self.event_handler.setTimeoutYOLO(num)
        self.timeoutWatchdog = num

    def run(self):
        self.observer.schedule(self.event_handler, path=IMG_PATH, recursive=True)
        self.observer.start()
        try:
            while True:
                if self.timeoutWatchdog != 0:
                    time.sleep(self.timeoutWatchdog/2)
                if self.isStopped:
                    break
                time.sleep(TIMESLEEPTHREAD)
        except KeyboardInterrupt:
            pass
            # self.stop()

    def start(self):
        self.handlerThread.start()

    def stop(self):
        self.isStopped = True
        self.observer.stop()
        time.sleep(TIMESLEEPTHREAD)
        self.observer.join()
        self.handlerThread.join()
        print("[]\tYOLO Stopping.....")

    def getYoloResult(self):
        return self.event_handler.getYoloResult()
    
if __name__=="__main__":
    # detector = YoloHandler()
    # detector.start()

    detector = YOLO(False)
    print(detector.detect("./image/coba.jpg"))
