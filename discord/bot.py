import asyncio
import locale
import os
import platform
import urllib.request
import re
import uuid
from urllib.parse import quote
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pytube import YouTube


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='-', intents=intents, activity=discord.Game(name="mineshare.top"))
bot.remove_command('help')

blacklist = ['пидарас', 'пидарасы', 'пидор', 'педик', 'пидр', 'гомик', 'faggot', 'хохол',
             'nigger', 'nigga', 'naga', 'ниггер', 'нига', 'нигер', 'нигга', 'даун', 'аутист']


@bot.event
async def on_ready():
    print('----- START -----')


@bot.event
async def on_member_join(ctx):
    role = discord.utils.get(ctx.guild.roles, name="📔 | Участник")
    await ctx.add_roles(role)


@bot.event
async def on_message(message):
    global blacklist
    role_admin = discord.utils.get(message.guild.roles, name="📕 | Администратор")
    if not role_admin in message.author.roles:
        if any(bad_word in message.content.lower() for bad_word in blacklist):
            await message.delete()
            embed = discord.Embed(description="Извините, ваше сообщение содержит запрещенные слова.",
                                  color=0x11b2ff)
            embed.set_author(name=message.author.display_name + "#" + message.author.discriminator,
                             icon_url=message.author.avatar)
            await message.channel.send(embed=embed, delete_after=8)
            return

        if "-play" in message.content and "youtube.com" in message.content.lower():
            await bot.process_commands(message)
            return
        elif "https" in message.content.lower():
            await message.delete()
            embed = discord.Embed(description="Извините, на данном сервере запрещено распространение стронних ссылок.",
                                  color=0x11b2ff)
            embed.set_author(name=message.author.display_name + "#" + message.author.discriminator,
                             icon_url=message.author.avatar)
            await message.channel.send(embed=embed, delete_after=8)
        elif "http" in message.content.lower():
            await message.delete()
            embed = discord.Embed(description="Извините, на данном сервере запрещено распространение стронних ссылок.",
                                  color=0x11b2ff)
            embed.set_author(name=message.author.display_name + "#" + message.author.discriminator,
                             icon_url=message.author)
            await message.channel.send(embed=embed, delete_after=8)
        elif ".ru" in message.content.lower():
            await message.delete()
            embed = discord.Embed(description="Извините, на данном сервере запрещено распространение стронних ссылок.",
                                  color=0x11b2ff)
            embed.set_author(name=message.author.display_name + "#" + message.author.discriminator,
                             icon_url=message.author)
            await message.channel.send(embed=embed, delete_after=8)
        elif ".com" in message.content.lower():
            await message.delete()
            embed = discord.Embed(description="Извините, на данном сервере запрещено распространение стронних ссылок.",
                                  color=0x11b2ff)
            embed.set_author(name=message.author.display_name + "#" + message.author.discriminator,
                             icon_url=message.author.avatar)
            await message.channel.send(embed=embed, delete_after=8)
        elif ".net" in message.content.lower():
            await message.delete()
            embed = discord.Embed(description="Извините, на данном сервере запрещено распространение стронних ссылок.",
                                  color=0x11b2ff)
            embed.set_author(name=message.author.display_name + "#" + message.author.discriminator,
                             icon_url=message.author.avatar)
            await message.channel.send(embed=embed, delete_after=8)

    await bot.process_commands(message)


@bot.command()
async def play(ctx, *, url):
    if not ctx.guild.voice_client in bot.voice_clients:
        try:
            channel = ctx.author.voice.channel
            await channel.connect()
        except:
            await ctx.message.delete()
            embed = discord.Embed(title="Mineshare - Музыка",
                                  description='Пожалуйста, зайдите в голосовой канал, чтобы использовать команды!',
                                  colour=0x11b2ff)
            await ctx.channel.send(embed=embed, delete_after=8)
            return

    if os.path.exists(os.getcwd() + "/" + "[" + str(ctx.message.guild.id) + "]"):
        directory = os.getcwd() + "/" + "[" + str(ctx.message.guild.id) + "]"
        print(f"[play] Директория уже существует: {directory}")
    else:
        directory = os.path.join(os.getcwd() + "/", "[" + str(ctx.message.guild.id) + "]")
        print(f"[play] Директория успешно создана: {directory}")

    if "youtube.com" in url:
        yt = YouTube(url)
    else:
        print(url)
        html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + quote(url).replace(" ", "+"))
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[0])

    embed = discord.Embed(title="Mineshare - Музыка", description="**Сейчас играет:** " + yt.title, colour=0x11b2ff)
    await ctx.channel.send(embed=embed)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="\"" + yt.title + "\""))

    video = yt.streams.get_audio_only()

    download_file = video.download(output_path=directory)

    out_file = directory + "/" + str(uuid.uuid4()) + '.mp3'
    os.rename(download_file, out_file)

    server = ctx.message.guild
    voice_channel = server.voice_client

    if voice_channel.is_playing():
        voice_channel.stop()

    voice_channel.volume = 100
    if platform.system() == 'Linux':
        voice_channel.play(discord.FFmpegPCMAudio(out_file))
    else:
        voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=out_file))


@bot.command()
async def replay(ctx):
    if not ctx.guild.voice_client in bot.voice_clients:
        try:
            channel = ctx.author.voice.channel
            await channel.connect()
        except:
            await ctx.message.delete()
            embed = discord.Embed(title="Mineshare - Музыка",
                                  description='Пожалуйста, зайдите в голосовой канал, чтобы использовать команды!',
                                  colour=0x11b2ff)
            await ctx.channel.send(embed=embed, delete_after=8)
            return

    if not os.path.isdir(os.getcwd() + "/" + "[" + str(ctx.message.guild.id) + "]"):
        embed = discord.Embed(title="Mineshare - Музыка",
                              description='Извините, но текущая композиция отсутствует!',
                              colour=0x11b2ff)
        await ctx.channel.send(embed=embed, delete_after=8)
    else:
        directory = os.getcwd() + "/" + "[" + str(ctx.message.guild.id) + "]"
        os.chdir(directory)
        print(f"[replay] Директория уже существует: {directory}")
        files = filter(os.path.isfile, os.listdir(directory))
        files = [os.path.join(directory, f) for f in files]
        print(f"[replay] Существующие композиции: {files}")
        files.sort(key=lambda x: os.path.getmtime(x))

        await ctx.message.delete()
        embed = discord.Embed(title="Mineshare - Музыка", description="Текущая композиция была запущена еще раз!",
                              colour=0x11b2ff)
        await ctx.channel.send(embed=embed)

        out_file = files[-1]

        server = ctx.message.guild
        voice_channel = server.voice_client

        if voice_channel.is_playing():
            voice_channel.stop()

        voice_channel.volume = 100
        if platform.system() == 'Linux':
            voice_channel.play(discord.FFmpegPCMAudio(out_file))
        else:
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=out_file))


@bot.command()
async def stop(ctx):
    try:
        voice_client = ctx.message.guild.voice_client

        if voice_client.is_playing():
            voice_client.stop()
            await voice_client.disconnect()
            await bot.change_presence(activity=discord.Game(name="mineshare.top"))

    except Exception as ex:
        return

bot.run(TOKEN)
