# camera.py - camera class for chickenrobot, a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

import cv2 as cv
import os
import pysftp
from settings import *

# CONSTANTS
DEBUG = False

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

    def _find_cams(self):
        """find usb cams"""
        self.cam_array = []
        for cam_num in range(MAX_CAMS):
            cam = cv.VideoCapture(cam_num)
            if cam is None or not cam.isOpened():
                if DEBUG: print("DEBUG: Camera: camera", cam_num, "not found")
                pass
            else:
                self.cam_array.append(cam)
                if DEBUG: print("DEBUG: Camera: camera", cam_num, "found")
        self.num_cams = len(self.cam_array)

    def _setup_cams(self):
        """configure cams"""
        for cam in self.cam_array:
            cam.set(cv.CAP_PROP_FRAME_WIDTH, self.max_h)
            cam.set(cv.CAP_PROP_FRAME_HEIGHT, self.max_v)

    def take_image(self, cam_num):
        # capture image
        s, im = self.cam_array[cam_num].read()
        return(im)

    def take_all_images(self):
        self.image_array = []
        for cam_num in range(self.num_cams):
            self.image_array.append(self.take_image(cam_num))

    def write_images(self):
        for image_num in range(self.num_cams):
            filename = IMAGE_DIR + "image" + str(image_num) + ".jpg"
            if DEBUG: print("DEBUG: camera: filename:", filename)
            cv.imwrite(filename, self.image_array[image_num])

    def upload_images(self):
        with pysftp.Connection(host=SFTP_SERVER,
                               username=SFTP_USER,
                               password=SFTP_PASSWORD,
                               log=SFTP_LOG) as sftp:
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
        text = "Camera status:"
        for image_num in range(self.num_cams):
            text += "\n\tCamera " + str(image_num) + " in service"
        return text


def main():
    import sys

    if sys.platform != "darwin":
        MAX_HORZ = 1280
        MAX_VERT = 1024
    else:
        MAX_HORZ = 1920
        MAX_VERT = 1080

    camera = Camera(MAX_HORZ, MAX_VERT)
    print(camera.report())
    camera.take_and_upload_images()

if __name__ == '__main__':
    main()
