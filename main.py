from datetime import datetime
from discord_webhook import DiscordWebhook
import os
import asyncio
from sql_module_gh import fetch_ip_addresses

async def allCode(fail_streak):
    ip_addresses = await fetch_ip_addresses(fail_streak)
    for ip in ip_addresses:
        print("IP Address:", ip[0])
    return ip_addresses

async def send_webhook(formatted_time):

    ip = await allCode(1)
    ipid = ip[0]
    outtxt = formatted_time + " : " + str(ipid)

    try:
        SOME_SECRET = os.environ["SOME_SECRET"]
        thisurl = f"https://discordapp.com/api/webhooks/{SOME_SECRET}"
        webhook = DiscordWebhook(url=thisurl, content=outtxt)
        response = webhook.execute()
    except KeyError:
        SOME_SECRET = "Token not available!"

    return

# Get current date and time
current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

# Run the async function
asyncio.run(send_webhook(formatted_time))

# Write to file
with open('current_datetime.txt', 'w') as f:
    f.write(f'Current Date and Time: {formatted_time}')
