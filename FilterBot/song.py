import os
import logging
import youtube_dl
from pyrogram import Client, filters
from pyrogram.types import Message

# enable logging
logging.basicConfig(level=logging.DEBUG)

app = Client("download_bot")


def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': '%(id)s.%(ext)s'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
        except Exception as e:
            raise e

    return filename



@app.on_message(filters.command("m"))
def text_handler(client, message: Message):
    try:
        # search for the song on youtube and get video url
        query = " ".join(message.text.split()[1:])
        with youtube_dl.YoutubeDL() as ydl:
            search_results = ydl.extract_info(f"ytsearch:{query}", download=False)['entries']
            video_url = search_results[0]['webpage_url']

        # download and send audio file to the user
        filename = download_audio(video_url)
        with open(filename, "rb") as f:
            client.send_audio(message.chat.id, f, title=query)

        # delete the downloaded audio file
        os.remove(filename)

    except Exception as e:
        message.reply(f"Sorry, I encountered an error while processing your request.\n{e}")
        logging.exception(e)
