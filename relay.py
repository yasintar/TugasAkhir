import RPi.GPIO as GPIO
import time
from threading import Thread
from constant import *

class Relay:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(RELAIS_1_GPIO, GPIO.OUT)
        self._yoloRes = tinyList()
        self.isStopped = False
        self.isTurnedOn = False
        self.relayRun = Thread(target=self.run, name="Relay")

    def turnOnRelay(self):
        self.isTurnedOn = True
        GPIO.output(RELAIS_1_GPIO, GPIO.HIGH)

    def turnOffRelay(self):
        self.isTurnedOn = False
        GPIO.output(RELAIS_1_GPIO, GPIO.LOW)

    def run(self):
        print("[]\RELAY Starting.....")
        while True:
            if len(self.getYoloResList()[True])>=3 and len(self.getYoloResList()[True])<=4:
                self.turnOnRelay()
            elif len(self.getYoloResList()[False])>=3 and len(self.getYoloResList()[False])<=4:
                self.turnOffRelay()
            else:
                continue
            
            if self.isStopped:
                break

            time.sleep(TIMESLEEPTHREAD)

    def start(self):
        self.relayRun.start()

    def stop(self):
        self.isStopped = True
        time.sleep(TIMESLEEPTHREAD)
        GPIO.cleanup()
        self.relayRun.join()
        print("[]\tRelay Stopping.....")

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

if __name__=="__main__":
    relay = Relay()
    while True:
        x = input()
        if str(x) == 'q':
            relay.stop()
            break
        elif str(x) == 'w':
            relay.turnOnRelay
        elif str(x) == 'e':
            relay.turnOffRelay
