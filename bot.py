import logging
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

log = logging.getLogger(__name__)

import os
import facebook
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler


API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", None)
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
TOKEN = os.environ.get("TOKEN", None)
LINKS = [x.lower() for x in os.environ.get("LINKS", "").split(" ")]
CHAT = [int(x) for x in os.environ.get("CHAT", "").split(" ")]
BLOCK = [x.lower() for x in os.environ.get("BLOCK", "").split(" ")]


fb = Client(
    name='fbBot',
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)


@fb.on_message(filters.channel)
async def link_handle(c, m):
    txt = m.text if m.text else m.caption
    if any(word in txt.lower() for word in BLOCK):
        return print('Blocked:', txt)
    if m.chat.id in CHAT and any(link in txt.lower() for link in LINKS):
        try:
            graph = facebook.GraphAPI(access_token=TOKEN)
            x = graph.put_object(parent_object='me', connection_name='feed', message=txt)
            print('Post ID: ', x, '\nMessage: ', txt)
        except Exception as e:
            print('Error: ', e)

if __name__ == '__main__':
    print('Started')
    fb.run()