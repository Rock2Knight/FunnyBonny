from discord.ext import commands
from discord.utils import get
import discord
from youtube_dl import YoutubeDL
import ffmpeg
import os
from typing import Optional

intents = discord.Intents.default()
intents.message_content = True

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

TOKEN = ''
with open('.\\token.txt', 'r', encoding='utf-8') as tok:
    TOKEN = tok.read()
    tok.close()

voice = None
bot = commands.Bot(intents = intents, command_prefix='fb!')

server, server_id, name_channel = None, None, None

domains = ['https://www.youtube.com/', 'http://www.youtube.com/', 'https://youtu.be/', 'http://youtu.be/']


async def check_domains(link: str):
    for x in domains:
        if link.find(x) != -1:
            return True
    return False;


@bot.event
async def on_ready():
    print('Ready on 100%\n')


@bot.command(alliases=['do', 'will'])
async def Hello(ctx):
    await ctx.send('Hello, my dear!')


@bot.command()
async def coolBand(ctx):
    embed = discord.Embed(
        title='Of course, Linkin Park is coolest band!',
        description='Click here to come to top article',
        url='https://brodude.ru/9-sposobov-razvit-vnutrennij-sterzhen/'
    )
    await ctx.send(embed=embed)


@bot.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)  # Проходимся по списку голосовых каналов
                                                     # и получаем голосовой канал,
                                                     # на котором находится отправитель
    if voice and voice.is_connected():               # Если голос подключен
        await voice.move_to(channel)                 # То перемещаем его в голосовой канал
    else:
        voice = await channel.connect()                             # Подключаем бота к голосовому каналу
        await ctx.send(f'FunnyBonny запрыгивает на: {channel}')

@bot.command()
async def play(ctx, *, url: Optional[str]):
    global voice
    info: Optional[str] = None

    with YoutubeDL(YDL_OPTIONS) as ydl:
        if 'https://' in url:
            info = ydl.extract_info(url, download=False)
        else:
            info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]

    link = info['formats'][0]['url']

    #author = ctx.author  # Кто отправил сообщение
    #track = './Mus2/One_More_Light.mp4'
    voice.play(discord.FFmpegPCMAudio(executable='ffmpeg\\ffmpeg.exe', source=link, **FFMPEG_OPTIONS))  # Проигрываем трек

bot.run(TOKEN)
