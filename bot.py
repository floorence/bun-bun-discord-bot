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
from selenium.webdriver.chrome.options import Options

import requests
from urllib.request import urlopen


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('GUILD_ID')

intent=discord.Intents.default()
intent.message_content = True

bot = discord.Client(intents=intent)

tree = app_commands.CommandTree(bot)

next_quote = ""

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == 'bun bun':
        await bun_pic(message)


@tree.command(name = "bunpic", description= "random pic of bun bun", guild = discord.Object(id=GUILD))
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
    print(randpic)
    file = discord.File("bun bun pics/" + randpic, filename=randpic)
    embed = discord.Embed()
    embed.set_image(url="attachment://" + randpic)
    await ctx.channel.send(file=file, embed=embed)

@tree.command(name = "addpic", description= "add pic of bun bun", guild = discord.Object(id=GUILD))
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

@tree.command(name= "quote", description = "ask bun bun for a motivational quote from Reddit!", guild = discord.Object(id=GUILD))
async def quote(interaction: discord.Interaction):
    await interaction.response.defer()
    global next_quote
    if next_quote == "":
        await interaction.followup.send("please wait a few seconds before requesting another quote")
    else:
        await interaction.followup.send(next_quote)
        next_quote = ""
    await get_next_quote()


async def get_next_quote():
    reddit = asyncpraw.Reddit(
        client_id='c9oCO-mAlCCGbhvFZ53Pfw',
        client_secret='AWe4VFzy9BaxnIPx2r-X8Px_kOOi3Q',
        user_agent='bun bun',
    )

    subreddit = await reddit.subreddit("quotes")
    posts = subreddit.hot(limit=1000)
    list = [gen async for gen in posts]
    a = random.randint(0, 999)
    submission = list[a]
    while submission.stickied or submission.selftext:
        a = random.randint(0, 999)
        submission = list[a]

    global next_quote
    next_quote = submission.title
    await reddit.close()


@tree.command(name="quote2", description = "ask bun bun for a motivational quote!", guild = discord.Object(id=GUILD))
async def quote2(interaction: discord.Interaction):
    await interaction.response.defer()

    url = "https://randomwordgenerator.com/motivational-quote.php"

    options = Options()
    options.add_argument("--headless")  # run in background
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36")

    browser = webdriver.Chrome(options=options)
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    span = soup.find("span", class_="support-sentence")

    if span:
        quote_text = span.contents[0].strip().strip('"')

        author_tag = span.find("i")
        author = author_tag.get_text(strip=True) if author_tag else "Unknown"

        await interaction.followup.send(quote_text + "\n\t-" + author)

    else:
        print("Quote not found!")
    browser.quit()



@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.id == GUILD:
            break

    await tree.sync(guild=discord.Object (id=GUILD))


    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    await get_next_quote()


bot.run(TOKEN)