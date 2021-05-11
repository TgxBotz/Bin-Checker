import requests
from telethon import events, Button, TelegramClient
import os
import logging


logging.basicConfig(level=logging.INFO)

API_ID = os.environ.get("API_ID", 6)
API_HASH = os.environ.get("API_HASH", None)
TOKEN = os.environ.get("TOKEN", None)
if not API_ID.isdigit():
    print("API_ID - Should be Integer. Exiting Bot.")
    exit()

try:
    bot = TelegramClient('bin', API_ID, API_HASH)
    bin = bot.start(bot_token=TOKEN)
except ApiIdInvalidError:
    print("Your API_ID or API_HASH is Invalid.")
    print("Bot is quitting.")
    exit()
except Exception as e:
    print(f"Error : {str(e)}")
    print("Bot is Exiting..")
    exit()

async def add_me():
    bin.me = await bin.get_me()
    

@bin.on(events.NewMessage(pattern="^[!?/]start$"))
async def start(event):
    if event.is_group:
        await event.reply("**Bin-Checker is Alive**")
        return
    await event.reply(f"**Heya {event.sender.first_name}**\nIts a Bin-Checker Bot To Check Your Bins Are Valid Or Not.", buttons=[
    [Button.url("Mʏ Sᴏᴜʀᴄᴇ Cᴏᴅᴇ", "https://github.com/TgxBotz/Bin-Checker")]
    ])

@bin.on(events.NewMessage(pattern="^[!?/]help$"))
async def help(event):
    text = """
**Welcome to HelpMenu:**

- /start - To Start Me :)
- /help - To Get Help Menu
- /bin - To check is your bin valid or not
"""
    await event.reply(text, buttons=[[Button.url("Mʏ Sᴏᴜʀᴄᴇ Cᴏᴅᴇ", "https://github.com/TgxBotz/Bin-Checker")]])

@bin.on(events.NewMessage(pattern="^[!?/]bin (.*?)"))
async def binc(event):
    xx = await event.reply("`Processing.....`")
    input = event.pattern_match.group(1)
    url = requests.get(f"https://bins-su-api.now.sh/api/{input}")
    res = url.json()
    me = bin.me.username
    r = res.get("data")
    if not r:
        return await xx.edit(f"**➤ Invalid Bin:**\n\n**Bin -** `{input}`\n**Status -** `Invalid Bin`\n\n**Checked By -** @{me}\n**User-ID - {event.sender_id}**")
    vendor = r.get('vendor')
    type = r.get('type')
    level = r.get('level')
    bank = r.get('bank')
    country = r.get('country')
    valid = f"""
<b>➤ Valid Bin:</b>

<b>Bin -</b> <code>{input}</code>
<b>Status -</b> <code>Valid Bin</code>
<b>Vendor -</b> <code>{vendor}</code>
<b>Type -</b> <code>{type}</code>
<b>Level -</b> <code>{level}</code>
<b>Bank -</b> <code>{bank}</code>
<b>Country -</b> <code>{country}</code>

<b>Checked By - @{me}</b>
<b>User-ID - {event.sender_id}</b>
"""
    await xx.edit(valid, parse_mode="HTML")
            
if __name__ == "__main__":
    print("Successfully Started")
    bin.loop.run_until_complete(add_me())
    bin.run_until_disconnected()
