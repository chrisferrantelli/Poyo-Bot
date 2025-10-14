import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.guilds = True
intents.members = True 

bot = commands.Bot(command_prefix='!', intents=intents)
bot.embed_color = discord.Color.blue()

@bot.event
async def setup_hook():
       for filename in os.listdir("./cogs"):
         if filename.endswith(".py"):
            try:
               await bot.load_extension(f"cogs.{filename[:-3]}")
               print(f"The {filename[:-3]} cog has loaded")
            except Exception as err:
               print(f"Unable to load {filename}: {err}")

@bot.event
async def on_ready():
   print(f'{bot.user} has connected to Discord!')

@bot.command()
async def poyohelp(ctx):
   embed = discord.Embed(
         title='PoyoBot Commands (working on adding more)',
         description='''**Commands:**
         !poyoball [question] - Kirby will respond to your yes/no question
         !ego [other user optional] - Run this command to measure your or someone elses ego
         !insult [other user optional] - Run this with or without a user to insult them
         !play_cope - Lets the bot join in VC and play a predefined sound
         !hack - Allows you to "hack" people [NOTE: Does not really hack :)]
         !tldr - Reply to a long post with !tldr to get the tldr version if you don't want to read
         !warnconfig - Allows you to add/remove trigger words for automod
         !warnuser - Warns a specified user
         !whitelist - Allows you to add a specified role to the whitelist allowing immunity
         !quote [sarcastic, valley-girl, genz] (leave blank if normal style) - Quotes a user in different styles
         '''
    )
   
   await ctx.send(embed=embed)

bot.run(TOKEN)