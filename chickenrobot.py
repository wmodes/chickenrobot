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
import logging

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
        # self.send_report_and_photos()
        while(1):
            #
            # Should the door be closed?
            #
            # Note: We don't test here if door is already closed
            # (door.is_closed()), because though it may take no action
            # with the doors, it might have to reset AUTO/MANUAL mode
            if self.light.is_dark():
                result = self.door.close_door_auto()
                # It will only return something if it moved the doors
                if result:
                    logging.info("Door status:" + result)
                    # self.comms.send_text(result)
                    self.send_report_and_photos()
            #
            # Should the door be open?
            #
            # Note: We don't test here if door is already open
            # (door.is_open()), because though it may take no action
            # with the doors, it might have to reset AUTO/MANUAL mode
            elif self.light.is_light():
                result = self.door.open_door_auto()
                # It will only return something if it moved the doors
                if result:
                    logging.info("Door status:" + result)
                    # self.comms.send_text(result)
                    self.send_report_and_photos()
            #
            # Check for messages
            #
            command_list = self.comms.check_for_commands()
            # print("command list:", command_list)
            if command_list:
                for request_num, cmd in command_list:
                    if cmd == "photo" or cmd == "image" or cmd == "picture":
                        self.comms.send_text_and_photos("Here's photos of the coop. ", request_num)
                    elif cmd == "close":
                        self.comms.send_text(self.door.close_door_manual(), request_num)
                    elif cmd == "open":
                        self.comms.send_text(self.door.open_door_manual(), request_num)
                    elif cmd == "status" or cmd == "report":
                        self.send_report_and_photos(request_num)
                    elif cmd == "door":
                        self.comms.send_text(self.door.report(), request_num)
                    elif cmd == "sunrise" or cmd == "sunset" or cmd == "light":
                        self.comms.send_text(self.light.report(), request_num)
                    elif cmd == "help":
                        txt = "Hi! I'm on duty. Helpful commands are status, photo, open, close, door, sunset, sunrise."
                        self.comms.send_text(txt, request_num)
            sleep(5)
                # print('.')

    def report(self):
        msg_text = ""
        msg_text += "Hi! I'm on duty. "
        msg_text += self.door.report()
        msg_text += self.camera.report()
        msg_text += self.light.report()
        return(msg_text)

    def send_report(self):
        self.comms.send_text(self.report())

    def send_report_and_photos(self, passed_num=None):
        self.comms.send_text(self.report(), passed_num)
        self.camera.take_and_upload_images()
        self.comms.send_text_and_photos("Here's photos of the coop. ", passed_num)

def main():
    logging.basicConfig(
        filename=LOG_FILENAME,
        # encoding='utf-8',
        filemode='w',
        format='%(asctime)s %(levelname)s:%(message)s',
        level=logging.DEBUG
    )
    logger = logging.getLogger()
    # logging.debug('This message should go to the log file')
    # logging.info('So should this')
    # logging.warning('And this, too')
    # logging.error('And non-ASCII stuff, too, like Øresund and Malmö')
    logging.info("Starting")

    # nuthin here yet
    chickenrobot = Chickenrobot()
    try:
        chickenrobot.on_duty()
    except KeyboardInterrupt:
        logging.info("I'm off duty.")
        logging.info("Finishing")

if __name__ == '__main__':
    main()
