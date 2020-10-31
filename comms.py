# comms.py - comms class for chickenrobot, a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

import random
from twilio.rest import Client
from settings import *

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
            print("Comms: Sending message to:", number)
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
            print("Comms: Sending message to:", number)
            message = self.client.messages.create(
                body = msg_text,
                from_ = self.origin_num,
                media_url=image_array,
                to = number
            )

    def check_for_commands(self):
        """check for commands via sms and respond"""
        #
        # ref: https://www.twilio.com/docs/sms/tutorials/how-to-retrieve-and-modify-message-history-python
        #
        messages = self.client.messages.list(to=ORIGIN_NUM,limit=20)
        if not messages:
            return None
        command_list = []
        for msg in messages:
            # check if on list of recipients
            if msg.from_ not in TARGET_NUMS:
                # no, kill it
                print("Comms: Deleting msg from", msg.from_, "Body:", msg.body)
                self.client.messages(msg.sid).delete()
                continue
            # act on command
            cmd = ""
            for keyword in COMMANDS:
                if keyword in msg.body.lower():
                    cmd = keyword
                    break
            command_list.append((msg.from_, cmd))
            print("Comms: Message received: From:", msg.from_, "Command:", cmd)
            # delete message
            self.client.messages(msg.sid).delete()
        return command_list


def main():
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
