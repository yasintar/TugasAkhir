from threading import Thread
import watchdog.events
import watchdog.observers
import contextlib
import cv2 as cv
import numpy as np
import time

from constant import *

class YOLO:
    def __init__(self, withNCS, weight=YOLO_WEIGHT, cfg=YOLO_CFG, stream=False):
        self.stream = stream
        self.images = []
        self.result = 0
        self.withNCS = withNCS
        if self.withNCS: 
            from openvino.inference_engine import IECore, IENetwork
            self.net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)
            inferEngine = IECore()
            inferNet = IENetwork(model=cfg, weights=weight)
            self.execNet = inferEngine.load_network(network=inferNet, device_name="VPU")
        else:
            self.net = cv.dnn.readNet(weight,cfg)

    def detect(self, image):    
        try:
            self.prepareImg(image=image)
            layer_names = self.net.getLayerNames()
            output_layers = [layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

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

    def detectWithNCS(self, image):
        netOutput = list(self.net.outputs.keys())
        image = cv.dnn.blobFromImage(image, YOLO_SCALE, YOLO_IMGSIZE, (0,0,0), True, crop=False)
        input_blob = next(iter(self.net.inputs))
        output = self.net.infer({input_blob: image})
        print(output)

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
    def __init__(self, withNCS):
        self.yoloDetector = YOLO(withNCS)
        self.yoloRes = None
        self.withNCS = withNCS
        watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.png'],
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

class YoloHandler(watchdog.observers.Observer):
    def __init__(self, withNCS):
        print("[]\tYOLO Starting.....")
        self.isStopped = False
        self.event_handler = EventHandler(withNCS)
        self.observer = watchdog.observers.Observer()
        self.handlerThread = Thread(target=self.run, name="YoloHandler")
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

    def run(self):
        self.observer.schedule(self.event_handler, path=IMG_PATH, recursive=True)
        self.observer.start()
        try:
            while True:
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
        time.sleep(2)
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