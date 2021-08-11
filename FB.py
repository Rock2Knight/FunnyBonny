from discord.ext import commands
import discord
import youtube_dl
import os
import ffmpeg

TOKEN = ''
with open('.\\token.txt', r, encoding='utf-8') as tok:
    TOKEN = tok.read()
    tok.close()

bot = commands.Bot(command_prefix=('fb!'))

server, server_id, name_channel = None, None, None

domains = ['https://www.youtube.com/', 'http://www.youtube.com/', 'https://youtu.be/', 'http://youtu.be/']
async def check_domains(link):
    for x in domains:
        if link.find(x)!=-1:
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
        title = 'Of course, Linkin Park is coolest band!',
        description = 'Click here to come to top article',
        url = 'https://brodude.ru/9-sposobov-razvit-vnutrennij-sterzhen/'
        )
    await ctx.send(embed=embed)

@bot.command()
async def play(ctx, *, song=None):
    author = ctx.author               #Кто отправил сообщение

    source = ''                       #Ссылка или файл
    if song==None:
        server = ctx.guild                        
        name_channel = author.voice.channel.name
        voice_channel = discord.utils.get(server.voice_channels, name = name_channel)
    
    params = song.split(' ')
    if len(params)==1:
        source = params[0]
        server = ctx.guild
        name_channel = author.voice.channel.name
        voice_channel = discord.utils.get(server.voice_channels, name = name_channel)
        print('param 1')
    elif len(params)==3:
        server_id = params[0]
        voice_id = params[1]
        source = params[2]
        try:
            server_id = int(server_id)
            voice_id = int(voice_id)
        except:
            await ctx.channel.send(f'{author.mention}, id сервера или войса должно быть число!')
            return
        print('param 3')
        server = bot.get_guild(server_id)
        voice_channel = discord.utils.get(server.voice_channels, id=voice_id)
    else:
        await ctx.channel.send(f'{author.mention}, command is incorrect')
        return

    voice = discord.utils.get(bot.voice_clients, guild = server)
    if voice is None:
        await voice_channel.connect()
        voice = discord.utils.get(bot.voice_clients, guild = server)

    begin, end = '', ''
    if source!='':
        begin = source[0:4]

    if source==None:
        pass
    elif begin=='http':                       #Обработка ссылки
        if not await check_domains(source):   #Проверка на соответсвие доменам youtube
            await ctx.channel.send(f'{author.mention} неразрешенная ссылка')
            return

        ydl_opts = {                         #Опции для youtube-dl
            'format': 'bestaduio/best',
            'postprocessors':[
                {
                    'key':'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }
            ],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([source])                     #Скачиваем аудио

        files = os.listdir('.')    #Получаем список файлов в папке программы
        track = ''

        for file in files:
            if file.find('.mp3')!=-1:
                track = file       

        voice.play(discord.FFmpegPCMAudio(track))     #Проигрываем трек
        #os.remove(track)                              #Удаление трэка
    else:
        voice.play(discord.FFmpegPCMAudio(f'Mus2/{source}'))


bot.run(TOKEN)
