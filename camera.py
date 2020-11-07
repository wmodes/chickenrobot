# camera.py - camera class for chickenrobot, a controller for a coop door and cam controller
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
import cv2 as cv
import os
from time import sleep
import pysftp
from settings import *
import logging

# CONSTANTS
LIGHT_OFF = 0
LIGHT_ON = 1

# NOTE: max resolution of the hbv-1615 is 1280x1024
# If you switch to another cam, you may have to adjust this

class Camera(object):
    """Takes photos with USB cameras"""

    def __init__(self, max_horz, max_vert):
        self.max_h = max_horz
        self.max_v = max_vert
        self.num_cams = 0
        self.cam_array = []
        self.image_array = []
        self._find_cams()
        self._setup_cams()
        GPIO.setup(CAMLIGHT_PIN, GPIO.OUT)

    def _find_cams(self):
        """find usb cams"""
        self.cam_array = []
        for cam_num in range(MAX_CAMS):
            cam = cv.VideoCapture(cam_num)
            if cam is None or not cam.isOpened():
                logging.debug("Camera:Camera " + str(cam_num) + " not found")
                pass
            else:
                self.cam_array.append(cam)
                logging.debug("Camera:Camera " + str(cam_num) + " found")
        self.num_cams = len(self.cam_array)

    def _setup_cams(self):
        """configure cams"""
        for cam in self.cam_array:
            # TODO: Handle exceptions
            cam.set(cv.CAP_PROP_FRAME_WIDTH, self.max_h)
            cam.set(cv.CAP_PROP_FRAME_HEIGHT, self.max_v)

    def _release_cams(self):
        """turn off cams after use"""
        for cam in self.cam_array:
            cam.release()
        self.cam_array = []

    def _take_image(self, cam_num):
        # capture image
        # TODO: Handle exceptions
        GPIO.output(CAMLIGHT_PIN, LIGHT_ON)
        sleep(500)
        s, im = self.cam_array[cam_num].read()
        sleep(500)
        GPIO.output(CAMLIGHT_PIN, LIGHT_OFF)
        return(im)

    def take_all_images(self):
        # self._find_cams()
        # self._setup_cams()
        self.image_array = []
        for cam_num in range(self.num_cams):
            self.image_array.append(self._take_image(cam_num))
        # self._release_cams()

    def write_images(self):
        for image_num in range(self.num_cams):
            filename = IMAGE_DIR + "image" + str(image_num) + ".jpg"
            logging.debug("Camera:Image filename:" + filename)
            cv.imwrite(filename, self.image_array[image_num])

    def upload_images(self):
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        # TODO: Handle exceptions
        with pysftp.Connection(host=SFTP_SERVER,
                               username=SFTP_USER,
                               password=SFTP_PASSWORD,
                               log=SFTP_LOG,
                               cnopts=cnopts) as sftp:
            with sftp.cd(SFTP_IMAGE_DIR):
                for image_num in range(self.num_cams):
                    filename = IMAGE_DIR + "image" + str(image_num) + ".jpg"
                    sftp.put(filename)

    def show_images(self):
        for image_num in range(self.num_cams):
            cv.imshow("Test Image", self.image_array[image_num])

    def take_and_upload_images(self):
        self.take_all_images()
        self.write_images()
        self.upload_images()

    def report(self):
        if self.num_cams == 0:
            text = "I have no camera watching. "
        if self.num_cams == 1:
            text = "I have one camera watching. "
        else:
            text = f"I have {self.num_cams} cameras watching. "
        logging.info("Report:" + text)
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

    if sys.platform != "darwin":
        MAX_HORZ = 1280
        MAX_VERT = 1024
    else:
        MAX_HORZ = 1920
        MAX_VERT = 1080

    camera = Camera(MAX_HORZ, MAX_VERT)
    logging.info(camera.report())
    camera.take_and_upload_images()

if __name__ == '__main__':
    main()
