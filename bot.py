# bot.py
import os
import random
import asyncpraw
import urllib

import discord
from discord import app_commands
import discord.ext
from dotenv import load_dotenv
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver

import requests
from urllib.request import urlopen


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intent=discord.Intents.default()
intent.message_content = True

bot = discord.Client(intents=intent)

tree = app_commands.CommandTree(bot)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return



    if message.content == 'bun bun':
        await bun_pic(message)




@tree.command(name = "bunpic", description= "random pic of bun bun", guild = discord.Object(id=833726209245315102))
async def bunpic(interaction:discord.Interaction):
    await interaction.response.defer()
    imgs = os.listdir("bun bun pics")
    randpic = random.choice(imgs)
    file = discord.File("bun bun pics/" + randpic, filename=randpic)
    embed = discord.Embed()
    embed.set_image(url="attachment://" + randpic)
    await interaction.followup.send(file=file, embed=embed)

async def bun_pic(ctx):
    imgs = os.listdir("bun bun pics")
    randpic = random.choice(imgs)
    file = discord.File("bun bun pics/" + randpic, filename=randpic)
    embed = discord.Embed()
    embed.set_image(url="attachment://" + randpic)
    await ctx.channel.send(file=file, embed=embed)


@tree.command(name = "addpic", description= "add pic of bun bun [NOT DONE]", guild = discord.Object(id=833726209245315102))
async def addpic(interaction: discord.Interaction, file: discord.Attachment):
    await interaction.response.defer()

    if file:
        attachment_url = file.url
        file_request = requests.get(attachment_url, stream=True)
        img = Image.open(file_request.raw)
        files = os.listdir("bun bun pics")

        img.save("bun bun pics/bunpic" + str(len(files)) + ".png", 'png')
        await interaction.followup.send("new bun bun pic added!")
    else:
        await interaction.followup.send("please give an image")

@tree.command(name= "quote", description = "ask bun bun for a motivational quote!", guild = discord.Object(id=833726209245315102))
async def quote(interaction: discord.Interaction):
    await interaction.response.defer()
    # url = "https://randomwordgenerator.com/motivational-quote.php"
    """
    header = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7', }
    req = urllib.request.Request(url=url, headers=header)
    page = urllib.request.urlopen(req)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    print(html)
    
    browser = webdriver.Chrome()
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    quote = soup.find(id = 'result')

    print(soup)
    print(quote)
    browser.close()
    """
    """
       i = 0
       async for submission in posts:
           if (not submission.stickied) and (not submission.selftext):
               if i == a:
                   await interaction.followup.send(submission.title)
                   break
               i = i + 1
     """
    reddit = asyncpraw.Reddit(
        client_id='c9oCO-mAlCCGbhvFZ53Pfw',
        client_secret='AWe4VFzy9BaxnIPx2r-X8Px_kOOi3Q',
        user_agent='bun bun',
    )

    subreddit = await reddit.subreddit("quotes")
    posts = subreddit.hot(limit = 1000)
    list = [gen async for gen in posts]
    a = random.randint(0, 999)
    submission = list[a]
    while submission.stickied or submission.selftext:
        a = random.randint(0, 999)
        submission = list[a]

    await interaction.followup.send(submission.title)
    await reddit.close()



@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    await tree.sync(guild=discord.Object (id=833726209245315102))


    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )


bot.run(TOKEN)