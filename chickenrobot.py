# chickenrobot - a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

from comms import Comms
from light import Light
from door import Door
from camera import Camera
from settings import *

from time import sleep

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
        self.comms = Comms(ORIGIN_NUM, TARGET_NUMS)
        self.light = Light(CITY_NAME, LATITUDE, LONGITUDE, SUNRISE_DELAY, SUNSET_DELAY)
        self.door = Door(REVS)
        self.camera = Camera(MAX_HORZ, MAX_VERT)

    def on_duty(self):
        # issue reports on start
        self.send_report_and_photos()
        while(1):
            if self.light.is_dark() and self.door.is_open():
                print("Door status: Door closing...")
                self.door.close_door()
                self.send_report_and_photos()
            elif self.light.is_light() and self.door.is_closed():
                print("Door status: Door opening...")
                self.door.open_door()
                self.send_report_and_photos()
            else:
                sleep(5)
                # print('.')

    def report(self):
        msg_text = ""
        msg_text += "Chicken Robot: On duty." + '\n'
        msg_text += self.door.report() + '\n'
        msg_text += self.light.report() + '\n'
        msg_text += self.camera.report() + '\n'
        return(msg_text)

    def send_report(self):
        self.comms.send_text(self.report())

    def send_report_and_photos(self):
        self.comms.send_text(self.report())
        self.camera.take_and_upload_images()
        self.comms.send_text_and_photos("Here's photos of the coop")

def main():
    # nuthin here yet
    chickenrobot = Chickenrobot()
    try:
        chickenrobot.on_duty()
    except KeyboardInterrupt:
        print("\n\nChicken Robot: Off duty.")

if __name__ == '__main__':
    main()
