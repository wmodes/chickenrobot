import os
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()
# load_dotenv(verbose=True)

# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
         body='This is the ship that made the Kessel Run in fourteen parsecs?',
         from_='+18313370604',
         to='+18314190044'
     )

print(message.sid)
