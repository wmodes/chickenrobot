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

# Directions
CCW = 0    # Anti-clockwise rotation
CW = 1       # Clockwise rotation
# Door state
CLOSED = 0
OPEN = 1
# Door modes
AUTO = 0
MANUAL = 1

STEP_COUNT = SPR
STEP_DELAY = 1 / SPR   # 1 second / SPR

class Door(object):
    """class to open and close coop door and report on status"""

    def __init__(self, revs):
        self.revs = revs
        self.status = None
        self.mode = AUTO
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

    def open_door_auto(self):
        if self.mode == AUTO:
            if self.status == OPEN:
                return "The doors are already open. "
            else:
                self._move_door(OPEN)
                return "I just opened the doors. "
        else:
            if self.status == OPEN:
                # return to AUTO mode
                self.mode = AUTO
                return "The doors are already open. Resuming AUTOMATIC mode. "
            else:
                # manual mode overrides auto - doors stay closed
                return None

    def close_door_auto(self):
        if self.mode == AUTO:
            if self.status == CLOSED:
                return "The doors are already closed. "
            else:
                self._move_door(CLOSED)
                return "I just closed the doors. "
        else:
            if self.status == CLOSED:
                self.mode = AUTO
                return "The doors are already closed. Resuming AUTOMATIC mode. "
            else:
                # manual mode overrides auto - doors stay open
                return None

    def open_door_manual(self):
        if self.status == OPEN:
            # switch to auto mode, so door will auto close at sunset
            self.mode = AUTO
            return "The doors are already open. "
        else:
            # switch to manual mode, so auto will not override door
            self.mode = MANUAL
            self._move_door(OPEN)
            return "I just opened the doors. "

    def close_door_manual(self):
        if self.status == CLOSED:
            # switch to auto mode, so door will auto open at sunrise
            self.mode = AUTO
            return "The doors are already closed. "
        else:
            # switch to manual mode, so auto will not override door
            self.mode = MANUAL
            self._move_door(CLOSED)
            return "I just closed the doors. "

    def is_open(self):
        return self.status == OPEN

    def is_closed(self):
        return self.status == CLOSED

    def report(self):
        if self.status == CLOSED:
            # log "Door status: The door is currently CLOSED"
            txt = "The doors are currently CLOSED "
            if (self.mode == AUTO):
                txt += "in AUTOMATIC mode. "
            else:
                txt += "in MANUAL mode (AUTOMATIC resumes at sunrise). "
        else:
            # log "Door status: The door is currently OPEN"
            txt = "The doors are currently OPEN "
            if (self.mode == AUTO):
                txt += "in AUTOMATIC mode. "
            else:
                txt += "in MANUAL mode (AUTOMATIC resumes at sunset). "
        return txt

def main():
    print ("Platform:", sys.platform)
    revs = 10

    door = Door(revs)
    door.open_door_manual()
    print(door.report())

    sleep(1)
    door.close_door_manual()
    print(door.report())

if __name__ == '__main__':
    main()
