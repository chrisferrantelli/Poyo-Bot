import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set up intents
intents = discord.Intents.default()
intents.message_content = True

# Create bot instance
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
       for filename in os.listdir("./cogs"):

         if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"The {filename[:-3]} cog has loaded")

         else:
            print(f"Unable to load {filename[:-3]}")

         print(f'{bot.user} has connected to Discord!')



@bot.command()
async def help(ctx):
   embed = discord.Embed(
         title='PoyoBot Commands (working on adding more)',
         description='''**Commands:**
         !poyoball [question] - Kirby will respond to your yes/no question
         !ego [other user optional] - Run this command to measure your or someone elses ego
         !insult [other user optional] - Run this with or without a user to insult them
         !play_cope - Lets the bot join in VC and play a sound (needs work since the bot won't leave)
         '''
    )
   
   await ctx.send(embed=embed)

bot.run(TOKEN)