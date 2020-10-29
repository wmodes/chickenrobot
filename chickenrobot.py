# chickenrobot - a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

from light import Light
from door import Door
from camera import Camera

from time import sleep

# CONSTANTS
#
# Light class
# Felton, CA 37.0513° N, 122.0733° W
CITY_NAME = "Felton, CA"
LATITUDE = 37.0513
LONGITUDE = -122.0733
SUNRISE_DELAY = 0 # minutes
SUNSET_DELAY = 60 # minutes
#
# Camera class
MAX_HORZ = 1280
MAX_VERT = 1024
#
# Door class
REVS = 10   # number of revolutions to bring door up or lower it down

# General psuedocode
#
# Listen for text/email [comms]
# Respond to text/email [comms]
# 	Send photos [comms]
# 	Report status
# 	Open door
# 	Close door
# Check for sunrise / sunset triggers [chickenrobot]
# 	Sleep in between checks [chickenrobot]
# 	Close door [door]
# 	Open door [door]
# 	Send status [comms]
# 	Send photos [comms]
# Open door [door]
# Close door [door]
# Take photo [cam]
# Get sunrise / sunset times [light]

class Chickenrobot(object):
    """controller class for a coop door and cam controller"""
    def __init__(self):
        #
        # instantiate all our classes
        self.light = Light(CITY_NAME, LATITUDE, LONGITUDE, SUNRISE_DELAY, SUNSET_DELAY)
        self.door = Door(REVS)
        self.camera = Camera(MAX_HORZ, MAX_VERT)

        # issue reports on start
        self.door.report()
        self.light.report()
        self.camera.report()

    def on_duty(self):
        while(1):
            if self.light.is_dark() and self.door.is_open():
                self.door.close_door()
                self.report()
            elif self.light.is_light() and self.door.is_closed():
                self.door.open_door()
                self.report()
            else:
                sleep(5)
                # print('.')

    def report(self):
        print("Chicken Robot: On duty.")
        print(self.light.report())
        print(self.door.report())


def main():
    # nuthin here yet
    chickenrobot = Chickenrobot()
    chickenrobot.report()
    chickenrobot.on_duty()

if __name__ == '__main__':
    main()
