import discord
import random

from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
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

def setup(bot):
    bot.add_cog(Fun(bot))