import os
import discord
import asyncio
import sqlite3
import requests
import datetime
import bs4
import time
from discord.ext import commands
from youtube_dl import YoutubeDL
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio

bot = commands.Bot(command_prefix='#')
@bot.event
async def on_ready():
    print('=============================================')
    await asyncio.sleep(10) 
    print('[+]'+bot.user.name+'으로 접속됨')


@bot.command()
async def 접속(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        await ctx.send(embed = discord.Embed(title= "연결성공", description = "성공적으로 채널에 접속했어요", color = 0x00ff00))
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send(embed = discord.Embed(title= "연결실패", description = "먼저 음성채널에 접속하세요", color = 0x00ff0000))

@bot.command()
async def 나가(ctx):
    try:
        await vc.disconnect()
        await ctx.send(embed = discord.Embed(title= "연결해제", description = "그 채널에서 나갔습니다", color = 0x00ff00))
    except:
        await ctx.send(embed = discord.Embed(title= "연결해제 실패", description = "이미 그 채널에 속해있지 않아요", color = 0x00ff0000))


@bot.command()
async def 링크재생(ctx, *, url):
    YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "현재 " + url + "을(를) 재생하고 있습니다.", color = 0x00ff00))
    else:
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "이미 노래가 재생중입니다!", color = 0x00ff00))


@bot.command()
async def 재생(ctx, *, msg):
    if not vc.is_playing():
        options = webdriver.ChromeOptions()
        options.add_argument("headless")

        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                          'options': '-vn'}

        chromedriver_dir = r"C:\Users\uegeg\OneDrive\문서\Discord Bot\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir, options = options)
        driver.get("https://www.youtube.com/results?search_query=" + msg + "+lyrics")
        source = driver.page_source
        bs = bs4.BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[0]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com' + musicurl
        driver.quit()
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(
            embed=discord.Embed(title="노래 재생", description="현재 " + entireText + "을(를) 재생하고 있습니다.", color=0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "이미 노래가 재생 중이라 노래를 재생할 수 없어요!", color = 0x00ff00))

@bot.command()
async def 일시정지(ctx):
    if vc.is_playing():
        vc.pause()
        await ctx.send(embed = discord.Embed(title= "일시정지", description = entireText + "을(를) 일시정지 했습니다.", color = 0x00ff00))
    else:
        await ctx.send(embed = discord.Embed(title= "노래 재생", description = "노래가 재생중이지 않습니다.", color = 0x00ff00))

@bot.command()
async def 다시재생(ctx):
    try:
        vc.resume()
    except:
         await ctx.send(embed = discord.Embed(title= "다시재생 오류", description = "지금 노래가 재생되고 있지 않습니다", color = 0x00ff0000))
    else:
         await ctx.send(embed = discord.Embed(title= "다시재생", description = entireText  + "을(를) 다시 재생했습니다.", color = 0x00ff00))

@bot.command()
async def 노래끄기(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed = discord.Embed(title= "노래끄기", description = entireText  + "을(를) 종료했습니다.", color = 0x00ff00))
    else:
        await ctx.send(embed = discord.Embed(title= "노래끄기 오류", description = "지금 노래가 재생되고 있지 않습니다", color = 0x00ff0000))



@bot.command()
async def 지금노래(ctx):
    if not vc.is_playing():
        await ctx.send(embed = discord.Embed(title= "지금노래 오류", description = "지금 노래가 재생되고 있지 않습니다", color = 0x00ff0000))

    else:
        await ctx.send(
            embed=discord.Embed(title="지금노래", description="현재 " + entireText + "을(를) 재생하고 있습니다.", color=0x00ff00))

access_token = os.environ['BOT_TOKEN']
bot.run(access_token)
