import asyncio
import random
import discord


from discord.ext import commands

class HackingCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.command()
    async def hack(self, ctx, user: discord.Member = None):
        
        progress = 0
        phrases = [
            "Stealing IP...",
            "DDOSing toaster...",
            "Uploading viruses...",
            "Hacking mainframe...",
            "Encrypting cat pics...",
            "Injecting memes...",
            "Mining starbits...",
            "Deploying chaos.exe...",
            "Stealing NFTs...",
            "Installing Limewire...",
            "(͡° ͜ʖ ͡°)",
            "Injecting T-virus...",
            "Ordering pineapple on pizza..."
        ]

        lost_items = [
            "Bitcoin",
            "artwork",
            "money",
            "NFTs",
            "Aol account",
            "System32 folder",
            "dignity",
            "family photos",
            "kitten videos",
            "memes",
            "Dark Souls saves"
        ]

        if (user == None or user == ctx.author):
            await ctx.send ("Hack someone else...")
            return
        
        msg = await ctx.send("Hacking started...") 

        while progress <= 20:
            filled = "🟩" * progress
            empty = "⬜️" * (20 - progress)
            percentage = int((progress/20)*100)
            phrase = random.choice(phrases)

            await msg.edit(content = (
                    f"Hacking {user.mention}\n"
                    f"{phrase}\n"
                    f"[{filled}{empty}] {percentage}%"
            ))

            await asyncio.sleep(0.4)
            progress += 1
        
        lost_item = random.choice(lost_items)
        await msg.edit(content=f"Hacking has completed, {user.mention} has lost their {lost_item}")


async def setup(bot):
     await bot.add_cog(HackingCog(bot))

