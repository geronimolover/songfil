
import requests
import os
import logging
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pyrogram import Client, filters
from pyrogram.types import Message

# enable logging
logging.basicConfig(level=logging.DEBUG)


# initialize the Spotify API client
client_credentials_manager = SpotifyClientCredentials(
    client_id='61dcb7d7bff442e3a54a3340825ade72',
    client_secret='ee316ec4c1e848078d9131c8922a343d'
)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def download_audio(url):
    response = requests.get(url)
    
    # save the audio file to disk
    filename = f"{url.split('=')[1]}.mp3"
    with open(filename, "wb") as f:
        f.write(response.content)

    return filename


@Client.on_message(filters.command("sp"))
def spotify_handler(client, message: Message):
    try:
        query = " ".join(message.text.split()[1:])
        result = spotify.search(q=query, limit=1)

        # extract uri and name of the song
        uri = result['tracks']['items'][0]['uri']
        name = result['tracks']['items'][0]['name']

        # get audio file of the song and upload it to Telegram
        audio_file_url = spotify.track(uri)['preview_url']
        filename = download_audio(audio_file_url)
        with open(filename, "rb") as f:
            client.send_audio(message.chat.id, f, title=name)

        # delete the downloaded audio file
        os.remove(filename)

    except Exception as e:
        message.reply(f"Sorry, I encountered an error while processing your request.\n{e}")
        logging.exception(e)
