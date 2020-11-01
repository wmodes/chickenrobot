import os
import pysftp
from dotenv import load_dotenv
load_dotenv()

SFTP_SERVER = 'sftp.sd5.gpaas.net'
SFTP_USER = '41496'
SFTP_IMAGE_DIR = '/lamp0/web/vhosts/modes.io/htdocs/interactive/chickenrobot/images'
SFTP_LOG = 'tmp/pysftp.log'
SFTP_PASSWORD = os.environ['SFTP_PASSWORD']

with pysftp.Connection(host=SFTP_SERVER,
                       username=SFTP_USER,
                       password=SFTP_PASSWORD,
                       log=SFTP_LOG) as sftp:
    with sftp.cd(SFTP_IMAGE_DIR):
        sftp.put('images/image0.jpg')
        sftp.put('images/image1.jpg')
    # sftp.put_d('images', SFTP_IMAGE_DIR)

print("Uploaded!")

# Prevent ImportError: sys.meta_path is None, Python is likely shutting dow
pysftp.env.close()
