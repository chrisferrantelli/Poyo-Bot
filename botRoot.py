import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import aiohttp

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def poyosay(ctx):
    await ctx.send('Poyo!')


@bot.command()
async def poyoball(ctx, *, question):
  responses = [
        # Positive
        "POYO!",
        "Poyoooo!!",
        "POOYO! (double puff)",
        "POYOPOYO!!",
        "poyo. (nods firmly)",
        "Poyo~",
        "Po~yo? (hopeful bounce)",
        "poyo poyo poyo!",
        "poyo.",
        "POyO!! (with jazz hands)",

        # Uncertain
        "...poyo?",
        "poy...yo?",
        "(blushes) poy...",
        "p-p-poyo??",
        "*inhales deeply* ...poyoooooooooo",

        # Negative
        "poy-nah.",
        "PO—no. (record scratch)",
        "...noYO.",
        "poyo... (shakes head)",
        "poynope."
  ]

  await ctx.send(f'{random.choice(responses)}')

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

bot.run(TOKEN)