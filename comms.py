# comms.py - comms class for chickenrobot, a controller for a coop door and cam controller
# author: Wes Modes <wmodes@gmail.com>
# date: Oct 2020
# license: MIT

from twilio.rest import Client
from settings import *

# CONSTANTS

# Twilio response format:
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

class Comms(object):
    """Takes care of all outward communications"""

    def __init__(self, origin_num, target_nums):
        self.client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        self.origin_num = origin_num
        self.target_nums = target_nums

    def send_text(self, msg_text):
        msg_text = MSG_PREFIX + msg_text + MSG_POSTFIX
        for number in self.target_nums:
            message = self.client.messages.create(
                body = msg_text,
                from_ = self.origin_num,
                to = number
            )
            print(message.status)

    def send_text_and_photos(self, msg_text):
        msg_text = MSG_PREFIX + msg_text + MSG_POSTFIX
        image_array = []
        for num in range(NUM_CAMS):
            image_array.append(IMAGE_URL_BASE + str(num) + BASE_URL_POSTFIX)
        for number in self.target_nums:
            message = self.client.messages.create(
                body = msg_text,
                from_ = self.origin_num,
                media_url=image_array,
                to = number
            )
            print(message.status)

    def check_for_commands(self):
        pass

def main():
    comms = Comms(ORIGIN_NUM, TARGET_NUMS)
    # comms.send_text("Integrating classes")
    comms.send_text_and_photos("Here's some photos")

if __name__ == '__main__':
    main()
