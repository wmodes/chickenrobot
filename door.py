# door.py - door class for chickenrobota controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

import config
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
import logging

# Directions
CCW = 0    # Anti-clockwise rotation
CW = 1       # Clockwise rotation
# Door state
CLOSED = 0
OPEN = 1
# Door modes
AUTO = 0
MANUAL = 1
# Indicator modes
LIGHT_OFF = 1
LIGHT_ON = 0

STEP_COUNT = config.SPR
STEP_DELAY = 1 / config.SPR   # 1 second / SPR

class Door(object):
    """class to open and close coop door and report on status"""

    def __init__(self, revs):
        self.revs = revs
        self.status = None
        self.mode = AUTO
        self._read_door_state()
        GPIO.setwarnings(False)
        GPIO.setmode(config.PINOUT_SCHEME)
        GPIO.setup(config.DIR_PIN, GPIO.OUT)
        GPIO.setup(config.STEP_PIN, GPIO.OUT)
        GPIO.setup(config.INDICATOR_PIN, GPIO.OUT)

    def _store_door_state(self):
        with open(config.DOOR_STATE_FILE, 'w') as file:
            file.write("DOOR_STATUS=" + str(self.status))

    def _read_door_state(self):
        if (os.path.isfile(config.DOOR_STATE_FILE)):
            with open(config.DOOR_STATE_FILE, 'r') as file:
                line = file.read()
            try:
                self.status = int(line.split("=")[1].strip())
            except ValueError:
                self.status = CLOSED
        else:
            self.status = CLOSED
            self._store_door_state()

    def _set_indicator(self, state):
        if (state == OPEN):
            logging.info("Doors:Turning off indicator")
            GPIO.output(config.INDICATOR_PIN, LIGHT_OFF)
        else:
            logging.info("Doors:Turning on indicator")
            GPIO.output(config.INDICATOR_PIN, LIGHT_ON)


    def _move_door(self, state):
        GPIO.output(config.DIR_PIN, state)
        for x in range(self.revs * STEP_COUNT):
            GPIO.output(config.STEP_PIN, GPIO.HIGH)
            sleep(STEP_DELAY)
            GPIO.output(config.STEP_PIN, GPIO.LOW)
            sleep(STEP_DELAY)
        # set indicator light
        self._set_indicator(state)
        # record status
        self.status = state
        self._store_door_state()

    def open_door_auto(self):
        # if we are in auto mode
        if self.mode == AUTO:
            if self.status == OPEN:
                # The doors are already open
                # logging.info("Doors:Doors are already open (AUTO)")
                return None
            else:
                logging.info("Doors:Open request received (AUTO)")
                self._move_door(OPEN)
                logging.info("Doors:Opened the doors (AUTO)")
                return "I just opened the doors. "
        # if we are in MANUAL mode
        else:
            # if the doors are OPEN
            if self.status == OPEN:
                logging.info("Doors:Open request received (AUTO)")
                # return to AUTO mode
                self.mode = AUTO
                # The doors are already open
                logging.info("Doors:Switch to AUTO mode; already open")
                return None
            # if the doors are CLOSED
            else:
                # manual mode overrides auto - doors stay closed
                logging.debug("Doors:Remain in MANUAL mode; stay closed")
                return None

    def close_door_auto(self):
        # if we are in auto mode
        if self.mode == AUTO:
            if self.status == CLOSED:
                # The doors are already closed
                # logging.debug("Doors:Already closed (AUTO)")
                return None
            else:
                logging.info("Doors:Close request received (AUTO)")
                self._move_door(CLOSED)
                logging.info("Doors:Opened the doors (AUTO)")
                return "I just closed the doors. "
        # if we are in MANUAL mode
        else:
            # if the doors are OPEN
            if self.status == CLOSED:
                logging.info("Doors:Close request received (AUTO)")
                self.mode = AUTO
                # The doors are already closed
                return None
            # if the doors are CLOSED
            else:
                # manual mode overrides auto - doors stay open
                logging.debug("Doors:Remain in MANUAL mode; stay open")
                return None

    def open_door_manual(self):
        logging.info("Doors:Open request received (MANUAL)")
        if self.status == OPEN:
            # switch to auto mode, so door will auto close at sunset
            # self.mode = AUTO
            logging.info("Doors:Already open (MANUAL)")
            return "The doors are already open. "
        else:
            # switch to manual mode, so auto will not override door
            self.mode = MANUAL
            self._move_door(OPEN)
            logging.info("Doors:Opened the doors (MANUAL)")
            return "I just opened the doors. "

    def close_door_manual(self):
        logging.info("Doors:Close request received (MANUAL)")
        if self.status == CLOSED:
            # switch to auto mode, so door will auto open at sunrise
            self.mode = AUTO
            logging.info("Doors:Already closed (MANUAL)")
            return "The doors are already closed. "
        else:
            # switch to manual mode, so auto will not override door
            self.mode = MANUAL
            self._move_door(CLOSED)
            logging.info("Doors:Closed the doors (MANUAL)")
            return "I just closed the doors. "

    def is_open(self):
        return self.status == OPEN

    def is_closed(self):
        return self.status == CLOSED

    def is_open_and_auto(self):
        return self.status == OPEN

    def is_closed(self):
        return self.status == CLOSED

    def report(self):
        if self.status == CLOSED:
            # log "Door status: The door is currently CLOSED"
            text = "The doors are currently CLOSED "
            if (self.mode == AUTO):
                text += "in AUTOMATIC mode. "
            else:
                text += "in MANUAL mode (AUTOMATIC resumes at sunrise). "
        else:
            # log "Door status: The door is currently OPEN"
            text = "The doors are currently OPEN "
            if (self.mode == AUTO):
                text += "in AUTOMATIC mode. "
            else:
                text += "in MANUAL mode (AUTOMATIC resumes at sunset). "
        logging.info("Doors:Report:%s", text)
        return text

def main():
    import sys
    logging.basicConfig(
        filename=sys.stderr,
        encoding='utf-8',
        format='%(asctime)s %(levelname)s:%(message)s',
        level=logging.DEBUG
    )
    logger = logging.getLogger()
    logging.info("Platform:" + sys.platform)
    revs = 10

    door = Door(revs)
    door.open_door_manual()
    logging.info(door.report())

    sleep(1)
    door.close_door_manual()
    logging.info(door.report())

if __name__ == '__main__':
    main()
