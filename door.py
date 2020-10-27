# door.py - door class for chickenrobota controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

import sys
if sys.platform == "darwin":
    # OS X
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
    # sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)
import RPi.GPIO as GPIO
from time import sleep

DIR = 20    # Direction GPIO pin
STEP = 21   # Step GPIO pin
CW = 1      # Clockwise rotation
CCW = 0     # Anti-clockwise rotation
SPR = 200    # Steps per revolution (360/1.8) from stepper datasheet
CLOSED = 0
OPEN = 1

step_count = SPR
delay = 0.005   # 1 second / SPR

class Door(object):
    """class to open and close coop door and report on status"""

    def __init__(self, revs):
        self.revs = revs
        self.status = CLOSED
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)

    def _move_door(self, direction):
        GPIO.output(DIR, direction)
        for x in range(self.revs * step_count):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)

    def open_door(self):
        self._move_door(CW)
        self.status = OPEN

    def chose_door(self):
        self._move_door(CCW)
        self.status = CLOSED

    def is_open(self):
        return self.status == OPEN

    def is_closed(self):
        return self.status == CLOSED

    def report(self):
        if self.status == CLOSED:
            return "Door status: The door is currently CLOSED"
        else:
            return "Door status: The door is currently OPEN"


def main():
    print ("Platform:", sys.platform)
    revs = 10

    door = Door(revs)
    door.open_door()
    print(door.report())

    sleep(1)
    door.close_door()
    print(door.report())

if __name__ == '__main__':
    main()
