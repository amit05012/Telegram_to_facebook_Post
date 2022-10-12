# importing needs
from os import environ
from facebook import GraphAPI
from pyrogram import Client, filters


# Getting the useful values 
API_ID = int(environ.get("API_ID", 0))
API_HASH = environ.get("API_HASH", None)
BOT_TOKEN = environ.get("BOT_TOKEN", None)

TOKEN = [x for x in environ.get("TOKEN", "").split(" ")]
CHAT = [int(x) for x in environ.get("CHAT", "").split(" ")]
if len(CHAT) != len(TOKEN):
    # stopping code if number of tokens provided not equal to number of channels provided 
    print('Tg Channel number and fb page tokens number dosent match!!')

LINKS = [x.lower() for x in environ.get("LINKS", "").split(",")]
BLOCK = [x.lower() for x in environ.get("BLOCK", "").split(",")]


# Creating telegram client using pyrogram
fb = Client(
    name='fbBot',
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)


@fb.on_message(filters.channel)
async def link_handle(c, m):
    index = CHAT.index(m.chat.id) #getiing channel index
    txt = m.text if m.text else m.caption
    blocks = [i.strip() for i in BLOCK[index].split(" ")]
    links = [i.strip() for i in LINKS[index].split(" ")]
    if any(word in txt.lower() for word in blocks): #checking for blocked words
        return print('Blocked:', txt) #blocking blocked words
    if m.chat.id in CHAT and any(link in txt.lower() for link in links):
        try:
            graph = GraphAPI(access_token=TOKEN[index]) #creating facebook client
            post_id = graph.put_object(parent_object='me', connection_name='feed', message=txt) #posting message on facebook page
            print('Post ID: ', post_id, '\nMessage: ', txt)
        except Exception as e:
            print('Error: ', e)


if __name__ == '__main__' and len(CHAT) == len(TOKEN):
    print('Started your bot')
    fb.run()
    print('Bot has been stopped')
