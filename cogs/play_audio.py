import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

class PlayAudioCog(commands.Cog):
    load_dotenv()
    AUDIO_PATH = os.getenv('AUDIO_PATH')
    FFMPEG_PATH = os.getenv('FFMPEG_PATH')

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def play_cope(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("You are not in a voice channel")
            return
        
        vc = ctx.author.voice.channel
        voiceCha = ctx.voice_client

        if voiceCha and voiceCha.vc != vc:
            await voiceCha.move_to(vc)
        elif not voiceCha:
            voiceCha = await vc.connect()


        if voiceCha.is_playing():
            voiceCha.stop()
        
        voiceCha.play(discord.FFmpegPCMAudio(source=PlayAudioCog.AUDIO_PATH, executable=PlayAudioCog.FFMPEG_PATH))

        try: 
            while voiceCha.is_playing():
                await asyncio.sleep(1)
        
        finally:
            await voiceCha.disconnect()

async def setup(bot):
    await bot.add_cog(PlayAudioCog(bot))