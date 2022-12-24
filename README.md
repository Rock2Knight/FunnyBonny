# FunnyBonny
My Discord music an entetainment bot

This bot plays songs in voice channels of Discord. Also it may play whole albums, seek playlists analyzing a ganre.
In future I will add card game which is based on anime series "PsychoPass". Cards for this game are in "Cards" directory

Current commands:
******************
fb!help - all the commands
fb!play voice_channel_id source - add song from source to voice channel with id voice_channel_id. Source is link on youtube video. This command is working too slowly now
fb!play source - add song from source (youtube link) to voice channel where you are 

******************
Commit "Bug fix №1 and command join" from:

Application couldn't create a bot due to new update of discord.py.
But this bug was fixed with adding string
    
    intents = discord.Intents.default()
    intents.message_content = True

to FB.py file.
    
Also I have added command "join" which let FunnyBonny join to voice channel

*****************
Commit "YouTube Downloader" from:

I added class Downloader, which let to load video or
audio from YouTube if you have url of this page.

*****************
Commit "FFmpeg Player" from 24.12.2022 21:17

I added ffmpeg and changed settings for youtube_dl. Also
I have changed function play. Now you can make bot to play
a track from YouTube video if apply:
fb!play "https://www.youtube.com/watch"