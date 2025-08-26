import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import aiohttp

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
AUDIO_PATH = os.getenv('AUDIO_PATH')
FFMPEG_PATH = os.getenv('FFMPEG_PATH')

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def setup_hook():
   await bot.load_extension("cogs.poyoball")


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def poyosay(ctx):
    await ctx.send('Poyo!')

@bot.command()
async def ego(ctx, user: discord.Member= None):
   if user == ctx.author or user == None:
      await ctx.send(f'Your ego is {random.randint(1,100)}%')
   else:
      await ctx.send(f'{user.mention}`s ego is {random.randint(1,100)}%')

@bot.command()
async def insult(ctx, user: discord.Member = None):
   api_url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
   async with aiohttp.ClientSession() as session:
    async with session.get(api_url) as resp:
        data = await resp.json()
        insultt = data["insult"]
        if resp.status == 200 and (user == ctx.author or user == None):
          await ctx.send(f'{insultt}')
        else:
          await ctx.send(f'{user.mention}: {insultt}')


@bot.command()
async def play_cope(ctx):
   if not ctx.message.author.voice:
      await ctx.send("You are not in a voice channel")
      return
   
   vc = ctx.message.author.voice.channel
   voiceCha = await vc.connect()
   await ctx.send(f"Joined {vc.name}")
   voiceCha.play(discord.FFmpegPCMAudio(source=AUDIO_PATH, executable=FFMPEG_PATH))

bot.run(TOKEN)