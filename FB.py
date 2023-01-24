from discord.ext import commands
from discord.utils import get
import discord

from youtube_dl import YoutubeDL
import ffmpeg
import os
from typing import List

from downloader import *

intents = discord.Intents.default()
intents.message_content = True

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
TOKEN = ''

with open('.\\token.txt', 'r', encoding='utf-8') as tok:
    TOKEN = tok.read()
    tok.close()

voice = None                                                  # Голосовой клиент
bot = commands.Bot(intents = intents, command_prefix='fb!')

server, server_id, name_channel = None, None, None
AudioQueue: List[str] = list()                           # Очередь треков
trackIndex: int = 0                                      # Номер текущего трека в очереди
downloader = Downloader()                                # Парсер для видео

# Виды доменов в YouTube
domains = ['https://www.youtube.com/', 'http://www.youtube.com/', 'https://youtu.be/', 'http://youtu.be/']


async def check_domains(link: str):
    for x in domains:
        if link.find(x) != -1:
            return True
    return False;


@bot.event
async def on_ready():
    print('Ready on 100%\n')


# Отладочная команда
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


''' Команда для подключения бота к каналу '''
@bot.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel       # Получаем канал, с которого автор послал сообщение
    voice = get(bot.voice_clients, guild=ctx.guild)  # Проходимся по списку голосовых каналов
                                                     # и получаем голосовой канал,
                                                     # на котором находится отправитель
    if voice and voice.is_connected():               # Если голос подключен
        await voice.move_to(channel)                 # То перемещаем его в голосовой канал
    else:
        voice = await channel.connect()                             # Подключаем бота к голосовому каналу
        await ctx.send(f'FunnyBonny запрыгивает на: {channel}')

''' Комманда для отключения бота от канала '''
@bot.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)       # Проходимся по списку голосовых каналов
                                                          # и получаем голосовой канал,
                                                          # на котором находится отправитель
    if voice and voice.is_connected():                    # Если голос подключен
        await voice.disconnect()                          # То отключаем его от голосового канала
        await ctx.send(f'FunnyBonny покинул: {channel}')
    else:
        await ctx.send(f'FunnyBonny покинул: {channel}')

# Проигрывание песни
async def playTrack(url):
    global voice

    # Загружаем аудио по ссылке
    with YoutubeDL(YDL_OPTIONS) as ydl:
        if 'https://' in url:
            if len(AudioQueue) == 1:
                info = ydl.extract_info(url, download=False)
            else:
                info = ydl.extract_info(AudioQueue[trackIndex], download=False)
        else:
            if len(AudioQueue) == 1:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
            else:
                info = ydl.extract_info(f"ytsearch:{AudioQueue[trackIndex]}", download=False)['entries'][0]

    link = info['formats'][0]['url']  # Получаем ссылку на аудио
    voice.play(discord.FFmpegPCMAudio(executable='ffmpeg\\ffmpeg.exe', source=link, **FFMPEG_OPTIONS))  # Проигрываем трек


@bot.command()
async def play(ctx, *, track: Optional[str]):
    global voice
    global trackIndex
    global AudioQueue
    info: Optional[str] = None

    AudioQueue.append(track)     # Добавляем трек в очередь

    if track[:5] == 'https':     # Если мы передали в аргумент команды url трэка,
        await playTrack(track)   # то сразу передаем песню в плеер
    else:
        url = downloader.parseAudio(track)   # В противном случае
        await playTrack(url)                 # сначала парсим youtube, Находим url трэка, а затем передаем его на плеер

@bot.command()
async def pause(ctx):
    global voice
    voice.pause()

@bot.command()
async def resume(ctx):
    global voice
    voice.resume()

@bot.command()
async def stop(ctx):
    global voice
    voice.stop()

# Добавление трека в очередь
@bot.command()
async def replay(ctx, *, url: Optional[str]):
    global voice
    global trackIndex
    global AudioQueue

    if not url:
        print('No link')
        return

    if not url in AudioQueue:
        AudioQueue.append(url)
        trackIndex += 1

    if voice.is_playing():
        await ctx.send('Track is playing now :)')


@bot.command()
async def skip(ctx):
    global trackIndex
    global AudioQueue

    if voice.is_playing():
        await stop(ctx)

    url = AudioQueue[trackIndex]
    await play(ctx, url=url)

@bot.command()
async def queue(ctx):
    global voice
    global trackIndex
    global AudioQueue

    msgQueue: Optional[str] = ''
    for i, url in enumerate(AudioQueue):
        msgQueue += str(i+1) + '. ' + url + '\n'

    if voice.is_playing():
        embed = discord.Embed(
            title='FunnyBonny audio queue',
            description=msgQueue
        )
        await ctx.send(embed=embed)

bot.run(TOKEN)
