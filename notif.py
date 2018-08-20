import os
from pushetta import Pushetta
API_KEY="apikey"
CHANNEL_NAME="channel"
p=Pushetta(API_KEY)
p.pushMessage(CHANNEL_NAME, "Someone is at your DOOR !")

