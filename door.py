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
import os.path
from settings import *

CCW = CLOSED = 0    # Anti-clockwise rotation
CW = OPEN = 1       # Clockwise rotation

STEP_COUNT = SPR
STEP_DELAY = 1 / SPR   # 1 second / SPR

class Door(object):
    """class to open and close coop door and report on status"""

    def __init__(self, revs):
        self.revs = revs
        self._read_door_state()
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DIR, GPIO.OUT)
        GPIO.setup(STEP, GPIO.OUT)

    def _store_door_state(self):
        with open(DOOR_STATE_FILE, 'w') as file:
            file.write("DOOR_STATUS=" + str(self.status))

    def _read_door_state(self):
        if (os.path.isfile(DOOR_STATE_FILE)):
            with open(DOOR_STATE_FILE, 'r') as file:
                line = file.read()
            try:
                self.status = int(line.split("=")[1].strip())
            except ValueError:
                self.status = CLOSED
        else:
            self.status = CLOSED
            self._store_door_state()

    def _move_door(self, direction):
        GPIO.output(DIR, direction)
        for x in range(self.revs * STEP_COUNT):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(STEP_DELAY)
            GPIO.output(STEP, GPIO.LOW)
            sleep(STEP_DELAY)
        self.status = direction
        self._store_door_state()

    def open_door(self):
        if self.status != OPEN:
            self._move_door(OPEN)
            return "I just opened the doors. "
        else:
            return "The doors are already open. "

    def close_door(self):
        if self.status != CLOSED:
            self._move_door(CLOSED)
            return "I just closed the doors. "
        else:
            return "The doors are already closed. "

    def is_open(self):
        return self.status == OPEN

    def is_closed(self):
        return self.status == CLOSED

    def report(self):
        if self.status == CLOSED:
            # log "Door status: The door is currently CLOSED"
            return "The doors are currently CLOSED. "
        else:
            # log "Door status: The door is currently OPEN"
            return "The doors are currently OPEN. "


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
