# settings.py - settings for chickenrobot, a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

import os, sys
from dotenv import load_dotenv
load_dotenv()

# Chickenrobot class
LOG_FILENAME = "logs/cr.log"

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
if sys.platform == "darwin":
    MAX_HORZ = 1920
    MAX_VERT = 1080
else:
    MAX_HORZ = 1280
    MAX_VERT = 1024
MAX_CAMS = 4
ACTIVE_CAMS = 0
IMAGE_FILE_BASE = "images/image"
IMAGE_FILE_POSTFIX = '.jpg'
IMAGE_URL_BASE = 'https://modes.io/interactive/chickenrobot/'
SFTP_SERVER = 'sftp.sd5.gpaas.net'
SFTP_USER = '41496'
SFTP_IMAGE_DIR = '/lamp0/web/vhosts/modes.io/htdocs/interactive/chickenrobot/images'
SFTP_LOG = 'logs/sftp.log'
SFTP_PASSWORD = os.environ['SFTP_PASSWORD']

# GPIO Configs
#
DIR_PIN = 20            # Direction GPIO pin
STEP_PIN = 21           # Step GPIO pin
CAMLIGHT_PIN = 19       # Activate camlight GPIO pin
INDICATOR_PIN = 26      # Activate indicator GPIO pin

# Door class
#
SPR = 200           # Steps per revolution (360/1.8) from stepper datasheet
REVS = 10           # number of revolutions to bring door up or lower it down
DOOR_STATE_FILE = "door.state"

# Comms class
#
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
MSG_PREFIX = "Message from Chicken Robot:\n"
MSG_POSTFIX = "\nBawwwk! 🐓🤖"
ORIGIN_NUM = '+18313370604'
# TARGET_NUMS = ['+18314190044', '+18312269992', '+17025929231']
TARGET_NUMS = ['+18314190044', '+18312269992']
# TARGET_NUMS = ['+18314190044']
