from datetime import datetime
from discord_webhook import DiscordWebhook
import os

# Get current date and time
current_time = datetime.now()

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
    webhook = DiscordWebhook(url="https://discordapp.com/api/webhooks/{SOME_SECRET}", content=current_time)
    response = webhook.execute()
except KeyError:
    SOME_SECRET = "Token not available!"

# Write to file
with open('current_datetime.txt', 'w') as f:
    f.write(f'Current Date and Time: {current_time} : {SOME_SECRET}')
