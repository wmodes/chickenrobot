# chickenrobot - a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

import config
from comms import Comms
from light import Light
from door import Door
from camera import Camera
from time import sleep
import logging
import pprint

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
        self.comms = Comms(config.ORIGIN_NUM, config.TARGET_NUMS)
        self.light = Light(config.CITY_NAME, config.LATITUDE, config.LONGITUDE, config.SUNRISE_DELAY, config.SUNSET_DELAY)
        self.door = Door(config.REVS)
        self.camera = Camera(config.MAX_HORZ, config.MAX_VERT)

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
                    logging.info("Robot:Door status:%s", result)
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
                    logging.info("Robot:Door status:%s", result)
                    # self.comms.send_text(result)
                    self.send_report_and_photos()
            #
            # Check for messages
            #
            command_list = self.comms.check_for_commands()
            # print("command list:", command_list)
            logging.debug("Robot:Received from Comms:Command list:%s", pprint.pformat(command_list, indent=4))
            if command_list:
                for request_num, cmd in command_list:
                    logging.info("Robot:Handling command from %s:%s ", request_num, cmd)
                    if cmd == "photo" or cmd == "image" or cmd == "picture":
                        filename_array = self.camera.take_and_upload_images()
                        self.comms.send_text_and_photos("Here's photos of the coop. ", filename_array, request_num)
                    elif cmd == "close":
                        self.comms.send_text(self.door.close_door_manual(), request_num)
                    elif cmd == "open":
                        self.comms.send_text(self.door.open_door_manual(), request_num)
                    elif cmd == "status" or cmd == "report":
                        self.send_report_and_photos(request_num)
                    elif cmd == "door":
                        self.comms.send_text(self.door.report(), request_num)
                    elif cmd == "sun" or cmd == "light":
                        self.comms.send_text(self.light.report(), request_num)
                    elif cmd == "cam":
                        self.comms.send_text(self.camera.report(), request_num)
                    else:
                        txt = "Hi! I'm on duty. Helpful commands are status, photo, open, close, doors, sunset, sunrise, cameras."
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
        filename_array = self.camera.take_and_upload_images()
        self.comms.send_text_and_photos("Here's photos of the coop. ", filename_array, passed_num)

def main():
    logging.basicConfig(
        filename=config.LOG_FILENAME,
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
    logging.info("Robot:Starting")

    # nuthin here yet
    chickenrobot = Chickenrobot()
    try:
        chickenrobot.on_duty()
    except KeyboardInterrupt:
        logging.info("Robot:I'm off duty.")
        logging.info("Robot:Finishing")

if __name__ == '__main__':
    main()
