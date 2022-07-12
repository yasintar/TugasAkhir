import watchdog.events
import watchdog.observers
import contextlib
import cv2 as cv
import numpy as np
import time

from constant import *

class YOLO:
    def __init__(self, weight=YOLO_WEIGHT, cfg=YOLO_CFG, stream=False):
        self.stream = stream
        self.images = []
        self.result = 0
        self.net = cv.dnn.readNet(weight,cfg)

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
                        
            return self.confiAvg(confidences)
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
        blob = cv.dnn.blobFromImage(image, YOLO_SCALE, YOLO_IMGSIZE, (0,0,0), True, crop=False)
        self.net.setInput(blob)

class EventHandler(watchdog.events.PatternMatchingEventHandler):
    def __init__(self):
        self.yoloDetector = YOLO()
        self.yoloRes = None
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.png'],
                                                             ignore_directories=True, case_sensitive=False)
  
    def on_created(self, event):
        print("Watchdog received created event - % s" % event.src_path[2:])
        result = self.yoloDetector.detect(str(event.src_path[2:]))
        self.setYoloResult(result)
        print("YOLO Res : ", self.getYoloResult())

    def setYoloResult(self, result):
        self.yoloRes = result

    def getYoloResult(self):
        return self.yoloRes

class YoloHandler(watchdog.observers.Observer):
    def __init__(self):
        print("[]\tYOLO Starting.....")
        self.isStopped = False
        self.event_handler = EventHandler()
        self.observer = watchdog.observers.Observer()
        self.agsTimeout = None

    def dispatch_events(self, *args, **kwargs):
        if not getattr(self, '_is_paused', False):
            super(EventHandler, self).dispatch_events(*args, **kwargs)

    def pause(self):
        self._is_paused = True

    def setAgsTimeout(self, num):
        self.agsTimeout = num

    def resume(self):
        if self.agsTimeout is not None:
            time.sleep(self.agsTimeout)
        else:
            time.sleep(self.timeout)  # allow interim events to be queued
        self.event_queue.queue.clear()
        self._is_paused = False

    @contextlib.contextmanager
    def ignore_events(self):
        self.pause()
        yield
        self.resume()

    def start(self):
        self.observer.schedule(self.event_handler, path=IMG_PATH, recursive=True)
        self.observer.start()
        try:
            while True:
                if self.isStopped:
                    break
                
                print("YOLO THREAD")
                time.sleep(TIMESLEEPTHREAD)
        except KeyboardInterrupt:
            print("KEYBOARD YOLO")
            pass
            # self.stop()

    def stop(self):
        self.isStopped = True
        self.observer.stop()
        time.sleep(2)
        self.observer.join()
        print("[]\tYOLO Stopping.....")

    def getYoloResult(self):
        return self.event_handler.getYoloResult()
    
if __name__=="__main__":
    # detector = YoloHandler()
    # detector.start()

    detector = YOLO()
    print(detector.detect("image/13-07-2022_00:09:29.png"))