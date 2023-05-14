import random 
from pyrogram import Client as FilterBot, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from configs import BOT_PICS, StartTxT, HelpTxT, AboutTxT, LOGGER
from FilterBot.database import db
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pyrogram import Client

# Initialize Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ.get("SPOTIPY_CLIENT_ID"), client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET")))

@Client.on_message(filters.text & filters.incoming)
async def get_song_details(client, message):
    song_name = message.text
    results = sp.search(q=song_name, limit=1)
    if results:
        # Send song name
        name = results['tracks']['items'][0]['name']
        
        # Send artist names
        artists = results['tracks']['items'][0]['artists']
        for artist in artists:
            art = artist['name']
        
        # Send album name
        album = results['tracks']['items'][0]['album']['name']
        
        # Get popularity details
        popularity = results['tracks']['items'][0]['popularity']
        
        # Create caption with song details
        caption = f"<b>{name}</b>\n\nArtist: {art}\nAlbum: {album}\nPopularity: {popularity} \n\n For now song files are not available. My developer is working on it. Keep supporting and add more members to the group"
        
        # Send thumbnail image URL
        thumbnail_url = results['tracks']['items'][0]['album']['images'][0]['url']
        await message.reply_photo(thumbnail_url, caption=caption)
        
    else:
        await message.reply_text("Sorry, couldn't find any matching results for that song name.")
        
@Client.on_message(filters.command("music"))
async def get_song_details(client, message):
    song_name = " ".join(message.text.split()[1:])
    results = sp.search(q=song_name, limit=1)
    if results:
        # Send song name
        name = results['tracks']['items'][0]['name']
        
        # Send artist names
        artists = results['tracks']['items'][0]['artists']
        for artist in artists:
            art = artist['name']
        
        # Send album name
        album = results['tracks']['items'][0]['album']['name']
        
        # Get popularity details
        popularity = results['tracks']['items'][0]['popularity']
        
        # Create caption with song details
        caption = f"<b>{name}</b>\n\nArtist: {art}\nAlbum: {album}\nPopularity: {popularity}"
        
        # Send thumbnail image URL
        thumbnail_url = results['tracks']['items'][0]['album']['images'][0]['url']
        await message.reply_photo(thumbnail_url, caption=caption)
        
    else:
        await message.reply_text("Sorry, couldn't find any matching results for that song name.")
        

@FilterBot.on_message(filters.private & filters.command("start"))
async def startCMD(client: FilterBot, message: Message):

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.first_name, message.from_user.id)

    bot = await client.get_me()
    keyboard = [[
      InlineKeyboardButton('Add Me To Your Chat', url=f"https://t.me/{bot.username}?startgroup=true")
      ],[
      InlineKeyboardButton('Help', callback_data='main#help'),
      InlineKeyboardButton('About', callback_data='main#about')
      ],[
      InlineKeyboardButton('Updates', url='https://t.me/check_this_channel'),
      InlineKeyboardButton('Group', url='t.me/song_requestgroup')
      ]]

    if "motech" == BOT_PICS[0]:
        await message.reply_text(text=StartTxT.format(mention=message.from_user.mention), reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await message.reply_photo(photo=random.choice(BOT_PICS), caption=StartTxT.format(mention=message.from_user.mention), reply_markup=InlineKeyboardMarkup(keyboard))



@FilterBot.on_message(filters.private & filters.command("help"))
async def helpCMD(client: FilterBot, message: Message):

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.first_name, message.from_user.id)

    keyboard = [[ InlineKeyboardButton('Home', callback_data='main#start'),
                  InlineKeyboardButton('Close', callback_data='main#close') ]]

    if "motech" == BOT_PICS[0]:
        await message.reply_text(text=HelpTxT.format(mention=message.from_user.mention), reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await message.reply_photo(photo=random.choice(BOT_PICS), caption=HelpTxT.format(mention=message.from_user.mention), reply_markup=InlineKeyboardMarkup(keyboard))

@FilterBot.on_message(filters.private & filters.command("about"))
async def aboutCMD(client: FilterBot, message: Message):

    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.first_name, message.from_user.id)

    keyboard = [[ InlineKeyboardButton('Book', url='https://t.me/Thedigital_library'),
                   InlineKeyboardButton('Music', url='t.me/song_requestgroup') ],
                [ InlineKeyboardButton('Home', callback_data='main#start'),
                  InlineKeyboardButton('Help', callback_data='main#help') ]]

    if "motech" == BOT_PICS[0]:
        await message.reply_text(text=AboutTxT.format(mention=message.from_user.mention), reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await message.reply_photo(photo=random.choice(BOT_PICS), caption=AboutTxT.format(mention=message.from_user.mention), reply_markup=InlineKeyboardMarkup(keyboard))


@FilterBot.on_callback_query(filters.regex('main'))
async def maincallback(client: FilterBot, message):

    try:
        x, type = message.data.split("#")
    except:
        await message.answer("Erorrrr....")
        await message.message.delete()
        return

    if type == "start":
        bot = await client.get_me()
        keyboard = [[ InlineKeyboardButton('Add Me To Your Chat', url=f"t.me/{bot.username}?startgroup=true") ],
                    [ InlineKeyboardButton('Help', callback_data='main#help'),
                      InlineKeyboardButton('About', callback_data='main#about') ],
                    [ InlineKeyboardButton('Update', url='t.me/mo_tech_yt'),
                      InlineKeyboardButton('Group', url='t.me/song_requestgroup') ]]
        await message.message.edit(text=StartTxT.format(mention=message.from_user.mention), reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)

    elif type == "help":
        keyboard = [[ InlineKeyboardButton('Home', callback_data='main#start'),
                      InlineKeyboardButton('Close', callback_data='main#close') ]]
        await message.message.edit(text=HelpTxT, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)

    elif type == "about":
        keyboard = [[ InlineKeyboardButton('Tutorial', url='https://youtu.be/hDGgPNgjo9o'),
                       InlineKeyboardButton('Repo', url='https://github.com/PR0FESS0R-99/FilterBot') ],
                    [ InlineKeyboardButton('Home', callback_data='main#start'),
                      InlineKeyboardButton('Help', callback_data='main#help') ]]
        await message.message.edit(text=AboutTxT, reply_markup=InlineKeyboardMarkup(keyboard), disable_web_page_preview=True)
