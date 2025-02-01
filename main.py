from datetime import datetime
from discord_webhook import DiscordWebhook
import os

# Get current date and time
current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
    thisurl = "https://discordapp.com/api/webhooks/{SOME_SECRET}"
    webhook = DiscordWebhook(url=thisurl, content=formatted_time)
    response = webhook.execute()
except KeyError:
    SOME_SECRET = "Token not available!"

# Write to file
with open('current_datetime.txt', 'w') as f:
    f.write(f'Current Date and Time: {formatted_time} : {SOME_SECRET}')
