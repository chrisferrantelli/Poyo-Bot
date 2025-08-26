import discord
import random

from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


@commands.command()
async def ego(ctx, user: discord.Member= None):
    if user == ctx.author or user == None:
        await ctx.send(f'Your ego is {random.randint(1,100)}%')
    else:
        await ctx.send(f'{user.mention}`s ego is {random.randint(1,100)}%')

async def setup(bot):
    await bot.add_cog(Fun(bot))
