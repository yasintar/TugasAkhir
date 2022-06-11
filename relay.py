import RPi.GPIO as GPIO
from threading import Thread
from constant import *

class Relay:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)
        self._yoloRes = tinyList()
        self.relayRun = Thread(target=self.run, name="Relay")

    def turnOnRelay(self):
        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)

    def turnOffRelay(self):
        GPIO.output(RELAIS_1_GPIO, GPIO.LOW)

    def run(self):
        while True:
            if len(self.getYoloResList()[True])>=3 and len(self.getYoloResList()[True])<=4:
                self.turnOnRelay()
            elif len(self.getYoloResList()[False])>=3 and len(self.getYoloResList()[False])<=4:
                self.turnOffRelay()
            else:
                continue

    def start(self):
        self.relayRun.start()

    def stop(self):
        self.relayRun.join()

    def appendYoloRes(self, res):
        self._yoloRes.push(res)

    def getYoloResList(self):
        return self._yoloRes.getList()

class tinyList:
    def __init__(self):
        self.maxLen = MAX_RELAY_LIST
        self.list = []

    def push(self, x):
        if len(self.list) == self.maxLen:
            self.list.pop(0)
        self.list.append(x)

    def getList(self):
        return self.list