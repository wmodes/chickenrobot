# comms.py - comms class for chickenrobot, a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

import random
from twilio.rest import Client
from settings import *
import logging

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
    "sunrise",
    "sunset",
    "light"
]

logger = logging.getLogger()

class Comms(object):
    """Takes care of all outward communications"""

    def __init__(self, origin_num, target_nums):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        self.origin_num = origin_num
        self.target_nums = target_nums

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
            "Yours truly &ctera, 🐓🤖"
        ])

    def send_text(self, msg_text, passed_num=None):
        if passed_num:
            my_target_nums = [passed_num]
        else:
            my_target_nums = self.target_nums
        msg_text = MSG_PREFIX + msg_text + "\n" + self.random_signoff()
        for number in my_target_nums:
            logging.info("Comms:Sending message to:" + number)
            # TODO: Handle exceptions
            message = self.client.messages.create(
                body = msg_text,
                from_ = self.origin_num,
                to = number
            )

    def send_text_and_photos(self, msg_text, passed_num=None):
        if passed_num:
            my_target_nums = [passed_num]
        else:
            my_target_nums = self.target_nums
        msg_text = MSG_PREFIX + msg_text + "\n" + self.random_signoff()
        image_array = []
        for num in range(NUM_CAMS):
            image_array.append(IMAGE_URL_BASE + str(num) + BASE_URL_POSTFIX)
        for number in my_target_nums:
            logging.info("Comms:Sending photos to:" + number)
            # TODO: Handle exceptions
            message = self.client.messages.create(
                body = msg_text,
                from_ = self.origin_num,
                media_url=image_array,
                to = number
            )

    def check_for_commands(self):
        """check for commands via sms and respond"""
        # ref: https://www.twilio.com/docs/sms/tutorials/how-to-retrieve-and-modify-message-history-python
        #
        # dial down loggging while we are in the twillio API
        # if we are not set to DEBUG level
        current_level = logger.level
        if (current_level < logging.DEBUG):
            logger.setLevel(logging.WARNING)
        # We fetch the list from the Twilio API
        # (and reverse it since it comes most recent first)
        # TODO: Handle exceptions
        messages = self.client.messages.list(to=ORIGIN_NUM,limit=10).reverse()
        # restore loggging
        logger.setLevel(current_level)
        if not messages:
            return None
        command_list = []
        for msg in messages:
            # check if on list of recipients
            if msg.from_ not in TARGET_NUMS:
                # no, kill it
                logging.debug("Comms:Deleting msg from number not in sub list from" + msg.from_ + "Body:" + msg.body)
                # TODO: Handle exceptions
                self.client.messages(msg.sid).delete()
                continue
            # act on command
            cmd = ""
            for keyword in COMMANDS:
                if keyword in msg.body.lower():
                    cmd = keyword
                    break
            command_list.append((msg.from_, cmd))
            logging.info("Comms:Message received: From:" + msg.from_ + "Command:" + cmd)
            # TODO: Delete command ONLY after succeess handling it?
            # delete message
            # TODO: Handle exceptions
            logging.debug("Comms:Deleting handled message")
            self.client.messages(msg.sid).delete()
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
    comms = Comms(ORIGIN_NUM, TARGET_NUMS)
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
