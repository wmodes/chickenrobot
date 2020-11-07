# settings.py - settings for chickenrobot, a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

import os
from dotenv import load_dotenv
load_dotenv()

# Chickenrobot class
LOG_FILENAME = "cr.log"

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
MAX_HORZ = 1280
MAX_VERT = 1024
MAX_CAMS = 4
NUM_CAMS = 2
IMAGE_DIR = "images/"
SFTP_SERVER = 'sftp.sd5.gpaas.net'
SFTP_USER = '41496'
SFTP_IMAGE_DIR = '/lamp0/web/vhosts/modes.io/htdocs/interactive/chickenrobot/images'
SFTP_LOG = 'tmp/pysftp.log'
SFTP_PASSWORD = os.environ['SFTP_PASSWORD']

# GPIO Configs
#
DIR_PIN = 20            # Direction GPIO pin
STEP_PIN = 21           # Step GPIO pin
CAMLIGHT_PIN = 23       # Activate camlight GPIO pin
INDICATOR_PIN = 24      # Activate indicator GPIO pin

# Door class
#
SPR = 200           # Steps per revolution (360/1.8) from stepper datasheet
REVS = 10           # number of revolutions to bring door up or lower it down
DOOR_STATE_FILE = "door.state"

# Comms class
#
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_AUTH_TOKEN = os.environ['TWILIO_AUTH_TOKEN']
IMAGE_URL_BASE = 'https://modes.io/interactive/chickenrobot/images/image'
BASE_URL_POSTFIX = '.jpg'
MSG_PREFIX = "Message from Chicken Robot:\n"
MSG_POSTFIX = "\nBawwwk! 🐓🤖"
ORIGIN_NUM = '+18313370604'
# TARGET_NUMS = ['+18314190044', '+18312269992', '+17025929231']
TARGET_NUMS = ['+18314190044', '+18312269992']
# TARGET_NUMS = ['+18314190044']
