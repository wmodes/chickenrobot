import os
from twilio.rest import Client
from settings import *

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

msg_text = MSG_PREFIX + "Look look look! This is the first test of Chicken Robot's outbound communication. Add to your contacts." + MSG_POSTFIX

image_array = []
for num in range(NUM_CAMS):
    image_array.append(IMAGE_URL_BASE + str(num) + BASE_URL_POSTFIX)

# numbers_to_message = ['+18314190044', '+18312269992', '+17025929231']
numbers_to_message = TARGET_NUMS
for number in numbers_to_message:
    message = client.messages.create(
        body = msg_text,
        from_ = SEND_NUM,
        media_url=image_array,
        to = number
    )
    print(message.status)

# response format:
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

print(message.status)
