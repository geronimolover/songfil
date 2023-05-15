from pyrogram import Client as FilterBot, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from FilterBot.database import db
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pyrogram import Client

# Initialize Spotify API credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ.get("SPOTIPY_CLIENT_ID"), client_secret=os.environ.get("SPOTIPY_CLIENT_SECRET")))
        
@Client.on_message(filters.text & filters.incoming)
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
