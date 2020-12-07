# settings.py - settings for chickenrobot, a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

import os, sys
from dotenv import load_dotenv
load_dotenv()
if sys.platform == "darwin":
    # OS X
    import fake_rpi
    sys.modules['RPi'] = fake_rpi.RPi     # Fake RPi
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO # Fake GPIO
    # sys.modules['smbus'] = fake_rpi.smbus # Fake smbus (I2C)
import RPi.GPIO as GPIO
import logging

# Chickenrobot class
LOG_FILENAME = "logs/cr.log"
LOG_LEVEL = logging.INFO

# Light class
#
# Felton, CA 37.0513° N, 122.0733° W
CITY_NAME = "Felton, CA"
LATITUDE = 37.0513
LONGITUDE = -122.0733
SUNRISE_DELAY = 0 # minutes
SUNSET_DELAY = 60 # minutes
TIME_FORMAT = '%-I:%M%p'

# Camera class
#
SFTP_LOG_LEVEL = logging.WARNING
if sys.platform == "darwin":
    MAX_HORZ = 1920
    MAX_VERT = 1080
else:
    MAX_HORZ = 1280
    MAX_VERT = 1024
MAX_CAMS = 8
ACTIVE_CAMS = 0

# Local file deets
#
IMAGE_DIR = "images"
IMAGE_FILE_BASE = IMAGE_DIR + "/image"
IMAGE_FILE_POSTFIX = '.jpg'
IMAGE_URL_BASE = 'https://modes.io/interactive/chickenrobot/'
DOOR_STATE_FILE = "door.state"
STATUS_FILE = "status.html"
NOIMAGE_FILE = "image-not-available.png"

# SFTP deets
#
SFTP_SERVER = 'sftp.sd5.gpaas.net'
SFTP_USER = '41496'
SFTP_IMAGE_DIR = '/lamp0/web/vhosts/modes.io/htdocs/interactive/chickenrobot/images'
SFTP_MAIN_DIR = '/lamp0/web/vhosts/modes.io/htdocs/interactive/chickenrobot'
SFTP_LOG = 'logs/sftp.log'
SFTP_PASSWORD = os.environ['SFTP_PASSWORD']

# GPIO Configs
#
DIR_PIN = 20            # Direction GPIO pin
STEP_PIN = 21           # Step GPIO pin
CAMLIGHT_PIN = 19       # Activate camlight GPIO pin
INDICATOR_PIN = 26      # Activate indicator GPIO pin
PINOUT_SCHEME = GPIO.BCM   # Boradcom pin numbering (NOT Wiring Pin numbering)

# Door class
#
SPR = 200           # Steps per revolution (360/1.8) from stepper datasheet
REVS = 10           # number of revolutions to bring door up or lower it down

# Comms class
#
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
TWILIO_LOG_LEVEL = logging.WARNING
MSG_POSTFIX = "\nBawwwk! 🐓🤖"
ORIGIN_NUM = '+18313370604'
# TARGET_NUMS = ['+18314190044', '+18312269992', '+17025929231']
TARGET_NUMS = ['+18314190044', '+18312269992']
# TARGET_NUMS = ['+18314190044']
IMG_STYLE = "width:300px;padding:5px;"
