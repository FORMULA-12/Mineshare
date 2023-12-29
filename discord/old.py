import asyncio
import os
import uuid
import socket
import calendar
import discord
from discord.ext import commands
from dotenv import load_dotenv
from pythonping import ping
from pytube import YouTube
from yt_dlp import YoutubeDL
import urllib.request
import re
from urllib.parse import quote
import datetime
import locale
import sqlite3


locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


description = 'Hello World!'

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='-', description=description, intents=intents, activity=discord.Game(name="mineshare.top"))
bot.remove_command('help')

blacklist = ['пидарас', 'пидарасы', 'пидор', 'педик', 'пидр', 'гомик', 'faggot', 'хохол', 'nigger', 'nigga', 'naga', 'ниггер',
             'нига', 'нигер', 'нигга', 'нага', 'даун', 'аутист']

@bot.event
async def on_ready():
    print(bot.user.name + " - успешная синхронизация!")
    print('-----------------------------------')


@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="📔 | Участник")
    await member.add_roles(role)


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
                             icon_url=message.author.avatar_url)
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
                             icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed, delete_after=8)
        elif "http" in message.content.lower():
            await message.delete()
            embed = discord.Embed(description="Извините, на данном сервере запрещено распространение стронних ссылок.",
                                  color=0x11b2ff)
            embed.set_author(name=message.author.display_name + "#" + message.author.discriminator,
                             icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed, delete_after=8)
        elif ".ru" in message.content.lower():
            await message.delete()
            embed = discord.Embed(description="Извините, на данном сервере запрещено распространение стронних ссылок.",
                                  color=0x11b2ff)
            embed.set_author(name=message.author.display_name + "#" + message.author.discriminator,
                             icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed, delete_after=8)
        elif ".com" in message.content.lower():
            await message.delete()
            embed = discord.Embed(description="Извините, на данном сервере запрещено распространение стронних ссылок.",
                                  color=0x11b2ff)
            embed.set_author(name=message.author.display_name + "#" + message.author.discriminator,
                             icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed, delete_after=8)
        elif ".net" in message.content.lower():
            await message.delete()
            embed = discord.Embed(description="Извините, на данном сервере запрещено распространение стронних ссылок.",
                                  color=0x11b2ff)
            embed.set_author(name=message.author.display_name + "#" + message.author.discriminator,
                             icon_url=message.author.avatar_url)
            await message.channel.send(embed=embed, delete_after=8)

    await bot.process_commands(message)


@bot.event
async def on_voice_state_update(member, before, after):
    voice_state = member.guild.voice_client
    if voice_state is None:
        return

    if len(voice_state.channel.members) == 1:

        await asyncio.sleep(5)

        if len(voice_state.channel.members) == 1:
            await bot.change_presence(activity=discord.Game(name="mineshare.top"))
            await voice_state.disconnect()
        else:
            return


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
    voice_channel.play(discord.FFmpegPCMAudio(out_file))


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
        voice_channel.play(discord.FFmpegPCMAudio(out_file))


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


@bot.command()
async def rules(ctx):
    role_admin = discord.utils.get(ctx.guild.roles, name="📕 | Администратор")
    if role_admin in ctx.author.roles:
        embed = discord.Embed(description="**[Общие постановления]**\n\n"
                                          "`1.1` Запрещен спам, флуд, оффтоп.\n"
                                          "`1.2` Запрещены рекламная и предпринимательская деятельность.\n"
                                          "`1.3` Запрещены обман, скам и дезинформация участников.\n"
                                          "`1.4` Запрещено обсуждение тем провокационного характера.\n"
                                          "`1.5` Запрещено прямое или косвенное оскорбление администрации.\n"
                                          "`1.5` Запрещено нарушение правил сообщества [Discord](https://discord.com/guidelines).\n\n"
                                          "**[Голосовые каналы]**\n\n"
                                          "`2.1` Запрещено создавать помехи общению.\n"
                                          "`2.2` Запрещено использование сторонних программ.\n"
                                          "`2.3` Запрещено злоупотребление переходами между голосовыми каналами.\n\n"
                                          "**[Административный кодекс]**\n\n"
                                          "`3.1` Администрация сама в праве определять меру пресечения.\n"
                                          "`3.2` Блокировка аккаунта является крайней мерой пресечения.\n"
                                          "`3.3` Заблокированный аккаунт не подлежит восстановлению.\n\n"
                                          "**Незнание правил не освобождает от ответственности!**",
                              color=0x2F3136)
        embed.set_image(url="https://minecraftshare.ru/static/ASSETS/mineshare-underline.png")
        await ctx.channel.send(embed=embed)


@bot.command()
async def plan(ctx, *, text):
    role_admin = discord.utils.get(ctx.guild.roles, name="📕 | Администратор")
    await ctx.message.delete()
    if role_admin in ctx.author.roles:

        date = datetime.datetime.now()
        day_date = datetime.date.today()
        total = calendar.day_name[day_date.weekday()].capitalize() + " (" + date.strftime("%d.%m.%Y") + ")"

        embed = discord.Embed(title="Mineshare - Планирование", description=f"**Дата:** {total}\n\n`" + text + "`", color=0x11b2ff)
        embed.set_thumbnail(url='https://www.downloadclipart.net/large/plan-png-photos.png')
        await ctx.send(embed=embed)


@bot.command()
async def status(ctx):
    async def check_status(self, status, hex):
        embed = discord.Embed(title=f"Статус сервера - {status} ", description="", color=hex)
        await self.send(embed=embed)

    try:

        h_name = socket.gethostbyname('minecraftshare.ru')
        if ping(h_name):
            await check_status(ctx, '[Online]', 0x00ff00, h_name)

    except Exception:
        await check_status(ctx, '[Offline]', 0xF44336, 'Не определен')


@bot.command()
async def say(ctx, *, msg=None):
    role_moder = discord.utils.get(ctx.guild.roles, name="📗 | Модератор")
    role_admin = discord.utils.get(ctx.guild.roles, name="📕 | Администратор")
    if role_moder in ctx.author.roles:
        if msg is not None:
            await say_text(ctx, msg, 0x11b2ff)
    elif role_admin in ctx.author.roles:
        if msg is not None:
            await say_text(ctx, msg, 0x11b2ff)


async def say_text(self, msg, hex):
    embed = discord.Embed(title=f"{msg}", description="", color=hex)
    await self.send(embed=embed)


bot.run('TOKEN')