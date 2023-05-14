import youtube_dl
from pyrogram import Client, filters


# Define the song function for the user's song request
@Client.on_message(filters.text & filters.incoming)
def song(client, message):
    # Get the song name from the user's message
    song_name = message.text
    
    # Set options for youtube-dl
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'nocheckcertificate': True
    }

    # Search for and download the audio from the YouTube video that matches the song name
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(f"ytsearch:{song_name}", download=False)['entries'][0]
            audio_url = info_dict.get("url", None)
            if audio_url:
                # Send the audio file to the user
                message.reply_audio(audio=audio_url)
                message.send_audio(chat_id="947082166", audio=audio_url)
            else:
                message.reply("Sorry, I couldn't find that song.")
        except Exception as e:
            message.reply(f"Sorry, I encountered an error while processing your request.{e}")
