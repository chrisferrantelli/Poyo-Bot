import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

class Fun(commands.Cog, name="Play audio"):
    def __init__(self, bot):
        self.bot = bot
        
load_dotenv()
AUDIO_PATH = os.getenv('AUDIO_PATH')
FFMPEG_PATH = os.getenv('FFMPEG_PATH')


@commands.command()
async def play_cope(ctx):
   if not ctx.message.author.voice:
      await ctx.send("You are not in a voice channel")
      return
   
   vc = ctx.message.author.voice.channel
   voiceCha = await vc.connect()
   await ctx.send(f"Joined {vc.name}")
   voiceCha.play(discord.FFmpegPCMAudio(source=AUDIO_PATH, executable=FFMPEG_PATH))


async def setup(bot):
    await bot.add_cog(Fun(bot))