import discord

from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def insult(ctx, user: discord.Member = None):
        api_url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                data = await resp.json()
                insultt = data["insult"]
                if resp.status == 200 and (user == ctx.author or user == None):
                    await ctx.send(f'{insultt}')
                else:
                    await ctx.send(f'{user.mention}, {insultt}')

async def setup(bot):
    await bot.add_cog(Fun(bot))