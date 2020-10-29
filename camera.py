# camera.py - camera class for chickenrobot, a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

import cv2 as cv

# CONSTANTS
MAX_CAMS = 4
IMAGE_DIR = "images/"
DEBUG = True

# NOTE: max resolution of the hbv-1615 is 1280x1024
# If you switch to another cam, you may have to adjust this

class Camera(object):
    """Takes photos with USB cameras"""

    def __init__(self, max_horz, max_vert):
        self.max_h = max_horz
        self.max_v = max_vert
        self.cap_array = []
        self.image_array = []
        self._find_cams()
        self._setup_cams()

    def _find_cams(self):
        """find usb cams"""
        self.cap_array = []
        for cap_num in range(MAX_CAMS):
            cap = cv.VideoCapture(cap_num)
            if cap is None or not cap.isOpened():
                print("Camera: camera", cap_num, "not found")
            else:
                self.cap_array.append(cap)
                print("Camera: camera", cap_num, "found")

    def _setup_cams(self):
        """configure cams"""
        for cam in self.cap_array:
            cam.set(cv.CAP_PROP_FRAME_WIDTH, self.max_h)
            cam.set(cv.CAP_PROP_FRAME_HEIGHT, self.max_v)

    def take_image(self, cam_num):
        # capture image
        s, im = self.cap_array[cam_num].read()
        return(im)

    def take_all_images(self):
        self.image_array = []
        for cam_num in range(len(self.cap_array)):
            self.image_array.append(self.take_image(cam_num))

    def write_images(self):
        for image_num in range(len(self.image_array)):
            filename = IMAGE_DIR + "image" + str(image_num) + ".jpg"
            if DEBUG: print("DEBUG: camera: filename:", filename)
            cv.imwrite(filename, self.image_array[image_num])

    def show_images(self):
        for image_num in range(len(self.image_array)):
            cv.imshow("Test Image", self.image_array[image_num])

def main():
    import sys
    if sys.platform != "darwin":
        MAX_HORZ = 1280
        MAX_VERT = 1024
    else:
        MAX_HORZ = 1920
        MAX_VERT = 1080

    camera = Camera(MAX_HORZ, MAX_VERT)
    camera.take_all_images()
    camera.write_images()

if __name__ == '__main__':
    main()
