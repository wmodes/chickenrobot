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

DIR = 20            # Direction GPIO pin
STEP = 21           # Step GPIO pin
CCW = CLOSED = 0    # Anti-clockwise rotation
CW = OPEN = 1       # Clockwise rotation
SPR = 200           # Steps per revolution (360/1.8) from stepper datasheet
DOOR_STATE_FILE = "door.state"

step_count = SPR
delay = 0.005   # 1 second / SPR

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
        for x in range(self.revs * step_count):
            GPIO.output(STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(STEP, GPIO.LOW)
            sleep(delay)
        self.status = direction
        self._store_door_state()

    def open_door(self):
        self._move_door(OPEN)

    def close_door(self):
        self._move_door(CLOSED)

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
