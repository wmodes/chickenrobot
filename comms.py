# comms.py - comms class for chickenrobot, a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

import config
import random
from twilio.rest import Client
import pysftp
import logging
import pprint
from datetime import datetime, timedelta

# CONSTANTS

COMMANDS = [
    "help",
    "photo",
    "image",
    "picture",
    "close",
    "open",
    "status",
    "report",
    "door",
    "sun",
    "light",
    "cam"
]

logger = logging.getLogger()
logging.getLogger('twilio.http_client').setLevel(logging.WARNING)

class Comms(object):
    """Takes care of all outward communications"""

    def __init__(self, origin_num, target_nums):
        self.client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
        self.origin_num = origin_num
        self.target_nums = target_nums
        self.last_fetch = datetime.now() - timedelta(minutes=60)

    def random_signon(self):
        return random.choice([
            "Message from Chicken Robot:\n",
            "Chicken Robot says:\n",
            "Chicken Robot sez:\n",
            "Chicken Robot says:\n",
            "Chicken Robot states:\n",
            "Chicken Robot reports:\n",
            "Here's what Chicken Robot reports:\n",
            "A missive from Chicken Robot:\n",
            "Communique from Chicken Robot:\n",
            "Chicken Robot issues this manifesto:\n"
        ])

    def random_signoff(self):
        return random.choice([
            "Bawwwk! 🐓🤖",
            "Love, 🐓🤖",
            "Hugs and kisses, 🐓🤖",
            "See ya, 🐓🤖",
            "Later, 🐓🤖",
            "Cheers, 🐓🤖",
            "Your friendly 🐓🤖",
            "Keep on, keepin' on, 🐓🤖",
            "Best regards, 🐓🤖"
            "All the best, 🐓🤖",
            "Regards, 🐓🤖",
            "Sincerely, 🐓🤖",
            "Respectfully, 🐓🤖",
            "Yours truly &c., 🐓🤖",
            "Sincerely and entirely yours, 🐓🤖",
            "Your friend, 🐓🤖",
            "Your sincere friend, 🐓🤖",
            "Yours with esteem, 🐓🤖",
            "Yours very respectfully, 🐓🤖",
            "Your affectionate father, 🐓🤖",
            "Ever yours, 🐓🤖",
            "Yours affectionately and forever, 🐓🤖",
            "Faithfully yours, 🐓🤖",
            "Ever your affectionate friend, 🐓🤖",
            "Yours heartily and affectionately, 🐓🤖",
            "Now and always your own, 🐓🤖",
            "Yours very sincerely, 🐓🤖",
            "Your obliged and affectionate friend, 🐓🤖",
            "Sincerely and entirely yours, 🐓🤖",
            "Regards, 🐓🤖",
            "Warmest Regards, 🐓🤖",
            "Cordially, 🐓🤖",
            "Cordially Yours, 🐓🤖",
            "Joyfully, 🐓🤖",
            "Keep looking up, 🐓🤖",
            "Keep the faith, 🐓🤖",
            "Keeping you in my prayers, 🐓🤖",
            "May God hug you tight with His love, 🐓🤖",
            "May your joy be full, 🐓🤖",
            "Rejoicing in Christ, 🐓🤖",
            "Your friend in Christ, 🐓🤖",
            "Your most humble servant and most faithful friend, 🐓🤖",
            "Yours expecting, 🐓🤖",
            "Adieu! take care of yourself; and, I entreat you, write! 🐓🤖",
            "With best love &c., 🐓🤖",
            "I kiss you, 🐓🤖",
            "Your old friend and erstwhile companion, 🐓🤖",
            "May your doom be other than mine, and your treasure remain with you to the end! 🐓🤖",
            "You bastard, 🐓🤖",
            "A tender adieu, 🐓🤖",
            "and my love+, 🐓🤖",
            "Yr sincere friend, 🐓🤖",
            "And I thank you for your attention, and I'm out of here, 🐓🤖"
        ])

    def send_text(self, msg_text, passed_num=None):
        if passed_num:
            my_target_nums = [passed_num]
        else:
            my_target_nums = self.target_nums
        msg_text = self.random_signon() + msg_text + "\n" + self.random_signoff()
        for phone_number in my_target_nums:
            logging.info("Comms:Sending msg to %s", phone_number)
            try:
                message = self.client.messages.create(
                    body = msg_text,
                    from_ = self.origin_num,
                    to = phone_number
                )
            except:
                logging.warning("Comms:Failed to send msg to %s:%s", phone_number, msg_text)

    def send_text_and_photos(self, msg_text, filename_array, passed_num=None):
        if passed_num:
            my_target_nums = [passed_num]
        else:
            my_target_nums = self.target_nums
        if not len(filename_array):
            msg_text = "No cameras available, so no photos."
        msg_text = self.random_signon() + msg_text + "\n" + self.random_signoff()
        image_array = []
        for filename in filename_array:
            image_url = config.IMAGE_URL_BASE + filename
            logging.debug("Comms:Image URL:%s", image_url)
            image_array.append(image_url)
        for phone_number in my_target_nums:
            logging.info("Comms:Sending photos to:%s", phone_number)
            try:
                message = self.client.messages.create(
                    body = msg_text,
                    from_ = self.origin_num,
                    media_url=image_array,
                    to = phone_number
                )
            except:
                logging.warning("Comms:Failed to send msg to %s:%s", phone_number, msg_text)

    def upload_status(self, status_text, image_text, filename_array):
        status_text = self.random_signon() + status_text + "\n"
        image_text = image_text + "\n" + self.random_signoff()
        html_text = ''
        # add status
        html_text += f'<div class="status"><pre style="white-space:pre-wrap;word-wrap:break-word;">{status_text}</pre></div>'
        # add photos
        html_text += '<div class="images">'
        if not len(filename_array):
            image_text = "No cameras available, so no photos."
        for filename in filename_array:
            image_url = config.IMAGE_URL_BASE + filename
            html_text += f'<img src="{image_url}" width=300>'
        html_text += '</div>'
        html_text += f'<div class="image-text"><pre>{image_text}</pre></div>'
        # print("html text:", html_text)
        # write status locally
        with open(config.STATUS_FILE, 'w') as out_file:
            out_file.write(html_text)
        # upload status
        logging.info("Comms:Uploading status")
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None
        try:
            with pysftp.Connection(host=config.SFTP_SERVER,
                                   username=config.SFTP_USER,
                                   password=config.SFTP_PASSWORD,
                                   log=config.SFTP_LOG,
                                   cnopts=cnopts) as sftp:
                with sftp.cd(config.SFTP_MAIN_DIR):
                    # upload files
                    logging.debug("Comms:Uploading status file via sftp")
                    sftp.put(config.STATUS_FILE)
        except:
            logging.warning("Comms:Failed to upload status")

    def check_for_commands(self):
        """check for commands via sms and respond"""
        # ref: https://www.twilio.com/docs/sms/tutorials/how-to-retrieve-and-modify-message-history-python
        #
        # We fetch the list from the Twilio API
        try:
            messages = self.client.messages.list(
                to=config.ORIGIN_NUM,
                date_sent_after=self.last_fetch - timedelta(minutes=15)
            )
            # if successful, record the date for our next fetch
            self.last_fetch = datetime.now()
        except:
            logging.warning("Comms:Failed to get msg list")
        # and reverse it since it comes most recent first
        messages.reverse()
        if not messages:
            logging.debug("Comms:No msgs found")
            return None
        else:
            for record in messages:
                logging.debug("Comms:Msg found:%s", record.sid)
        command_list = []
        for msg in messages:
            # check if msg not in list of recipients
            if msg.from_ not in config.TARGET_NUMS:
                # no, kill it
                logging.debug("Comms:Deleting msg from number not in sub list from $s:%s", msg.from_, msg.body)
                try:
                    self.client.messages(msg.sid).delete()
                except:
                    logging.warning("Comms:Failed to delete msg:sid %s", msg.sid)
                continue
            # look for command within msg
            cmd = ""
            for keyword in COMMANDS:
                if keyword in msg.body.lower():
                    cmd = keyword
                    break
            command_list.append((msg.from_, cmd))
            logging.info("Comms:Message received from %s:%s", msg.from_, cmd)
            # delete message
            logging.debug("Comms:Deleting handled message")
            try:
                self.client.messages(msg.sid).delete()
            except:
                logging.warning("Comms:Failed to delete msg:sid %s", msg.sid)
        logging.debug("Comms:Command list:%s", pprint.pformat(command_list, indent=4))
        return command_list

def main():
    import sys
    logging.basicConfig(
        filename=sys.stderr,
        encoding='utf-8',
        format='%(asctime)s %(levelname)s:%(message)s',
        level=logging.DEBUG
    )
    logger = logging.getLogger()
    comms = Comms(config.ORIGIN_NUM, config.TARGET_NUMS)
    # comms.send_text("Integrating classes")
    comms.send_text_and_photos("Here's some photos")

if __name__ == '__main__':
    main()


# REFERENCE

# Twilio sending sms/mms response format:
#
# {"sid": "SMxxxxxxxxxxxxxxx",
#  "date_created": "Thu, 09 Aug 2018 17:26:08 +0000",
#  "date_updated": "Thu, 09 Aug 2018 17:26:08 +0000",
#  "date_sent": null,
#  "account_sid": "ACxxxxxxxxxxxxxxxx",
#  "to": "+15558675310",
#  "from": "+15017122661",
#  "messaging_service_sid": null,
#  "body": "This is the ship that made the Kessel Run in fourteen parsecs?",
#  "status": "queued",
#  "num_segments": "1",
#  "num_media": "0",
#  "direction": "outbound-api",
#  "api_version": "2010-04-01",
#  "price": null,
#  "price_unit": "USD",
#  "error_code": null,
#  "error_message": null,
#  "uri": "/2010-04-01/Accounts/ACxxxxxxxxx/Messages/SMxxxxxxxxxxxx.json",
#  "subresource_uris": {
#      "media": null
#  }
# }

# Twilio request message format:
#
# "messages": [
#     {
#       "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#       "api_version": "2010-04-01",
#       "body": "testing",
#       "date_created": "Fri, 24 May 2019 17:44:46 +0000",
#       "date_sent": "Fri, 24 May 2019 17:44:50 +0000",
#       "date_updated": "Fri, 24 May 2019 17:44:50 +0000",
#       "direction": "outbound-api",
#       "error_code": null,
#       "error_message": null,
#       "from": "+12019235161",
#       "messaging_service_sid": null,
#       "num_media": "0",
#       "num_segments": "1",
#       "price": "-0.00750",
#       "price_unit": "USD",
#       "sid": "SMded05904ccb347238880ca9264e8fe1c",
#       "status": "sent",
#       "subresource_uris": {
#         "media": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMded05904ccb347238880ca9264e8fe1c/Media.json",
#         "feedback": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMded05904ccb347238880ca9264e8fe1c/Feedback.json"
#       },
#       "to": "+18182008801",
#       "uri": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Messages/SMded05904ccb347238880ca9264e8fe1c.json"
#     }
# ]
