# camera.py - camera class for chickenrobot, a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

import config
import sys
import os
import uuid
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
import logging

# CONSTANTS
LIGHT_OFF = 1
LIGHT_ON = 0

logging.getLogger("paramiko").setLevel(config.SFTP_LOG_LEVEL)
logging.getLogger('paramiko.transport').setLevel(config.SFTP_LOG_LEVEL)

# NOTE: max resolution of the hbv-1615 is 1280x1024
# If you switch to another cam, you may have to adjust this

class Camera(object):
    """Takes photos with USB cameras"""

    def __init__(self, max_horz, max_vert):
        self.max_h = max_horz
        self.max_v = max_vert
        self.cam_array = []
        self.image_array = []
        self._setup_camlight()
        self._find_cams()
        self._setup_cams()

    def _find_cams(self):
        """find usb cams"""
        self.cam_array = []
        for cam_num in range(config.MAX_CAMS):
            cam = cv.VideoCapture(cam_num)
            if cam is None or not cam.isOpened():
                logging.debug("Camera:Camera %s not found", str(cam_num))
                pass
            else:
                self.cam_array.append(cam)
                logging.debug("Camera:Camera %s found", str(cam_num))
        config.ACTIVE_CAMS = len(self.cam_array)
        logging.info("Camera:Active cameras:%s", str(config.ACTIVE_CAMS))

    def _setup_cams(self):
        """configure cams"""
        for cam in self.cam_array:
            try:
                cam.set(cv.CAP_PROP_FRAME_WIDTH, self.max_h)
                cam.set(cv.CAP_PROP_FRAME_HEIGHT, self.max_v)
            except:
                logging.warning("Camera:Failed to setup cameras (GPIO)")

    def _release_cams(self):
        """turn off cams after use"""
        for cam in self.cam_array:
            cam.release()
        self.cam_array = []

    def _take_image(self, cam_num):
        logging.debug("Camera:_take_image(%s)", str(cam_num))
        # capture image
        try:
            logging.info("Camera:Taking photo")
            s, im = self.cam_array[cam_num].read()
        except:
            logging.warning("Camera:Failed to take photo")
        return(im)

    def _take_all_images(self):
        self.turn_on_camlight()
        sleep(0.5)
        self.image_array = []
        for cam_num in range(config.ACTIVE_CAMS):
            self.image_array.append(self._take_image(cam_num))
        sleep(0.5)
        self.turn_off_camlight()
        # self._release_cams()

    def _write_images(self):
        filename_array = []
        logging.debug("Camera:write_images()")
        for image_num in range(config.ACTIVE_CAMS):
            filename = config.IMAGE_FILE_BASE + '.' + str(uuid.uuid4()) + '.' + str(image_num) + config.IMAGE_FILE_POSTFIX
            filename_array.append(filename)
            logging.debug("Camera:Image filename:%s", filename)
            cv.imwrite(filename, self.image_array[image_num])
        return filename_array

    def _upload_images(self, filename_array):
        logging.info("Camera:Uploading images")
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        try:
            with pysftp.Connection(host=config.SFTP_SERVER,
                                   username=config.SFTP_USER,
                                   password=config.SFTP_PASSWORD,
                                   log=config.SFTP_LOG,
                                   cnopts=cnopts) as sftp:
                with sftp.cd(config.SFTP_IMAGE_DIR):
                    # delete existing files
                    logging.debug("Camera:deleting old files via sftp")
                    for file in sftp.listdir():
                        sftp.remove(file)
                    # upload files
                    logging.debug("Camera:Uploading files via sftp")
                    for filename in filename_array:
                        sftp.put(filename)
        except:
            logging.warning("Camera:Failed to upload photos")

    def _cleanup_images(self):
        logging.info("Camera:Cleaning up local image files")
        for file in os.listdir(config.IMAGE_DIR):
            if not file.endswith(config.IMAGE_FILE_POSTFIX):
                continue
                os.remove(os.path.join(config.IMAGE_DIR, file))

    def show_images(self):
        for image_num in range(config.ACTIVE_CAMS):
            cv.imshow("Test Image", self.image_array[image_num])

    def take_and_upload_images(self):
        logging.debug("Camera:take_and_upload_images()")
        self._take_all_images()
        filename_array = self._write_images()
        self._upload_images(filename_array)
        self._cleanup_images()
        return filename_array

    def _setup_camlight(self):
        GPIO.setmode(config.PINOUT_SCHEME)
        GPIO.setup(config.CAMLIGHT_PIN, GPIO.OUT)

    def turn_on_camlight(self):
        logging.info("Camera:Turning on camlight")
        try:
            GPIO.output(config.CAMLIGHT_PIN, LIGHT_ON)
        except:
            logging.warning("Camera:Failed to turn on camlight (GPIO)")
        logging.debug("Camera:Camlight on")

    def turn_off_camlight(self):
        logging.info("Camera:Turning off camlight")
        try:
            GPIO.output(config.CAMLIGHT_PIN, LIGHT_OFF)
        except:
            logging.warning("Camera:Failed to turn off camlight (GPIO)")
        logging.debug("Camera:Camlight off")

    def report(self):
        if config.ACTIVE_CAMS == 0:
            text = "I have no camera watching. "
        if config.ACTIVE_CAMS == 1:
            text = "I have one camera watching. "
        else:
            text = f"I have {config.ACTIVE_CAMS} cameras watching. "
        logging.info("Camera:Report:%s", text)
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
        config.MAX_HORZ = 1280
        config.MAX_VERT = 1024
    else:
        config.MAX_HORZ = 1920
        config.MAX_VERT = 1080

    camera = Camera(config.MAX_HORZ, config.MAX_VERT)
    logging.info("Camera:Report:%s", camera.report())
    camera.take_and_upload_images()

if __name__ == '__main__':
    main()
