import discord
import random
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


from discord.ext import commands

class PoyoballCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    async def poyoball(self, ctx, *, question: str = None):

        if question is None:
            await ctx.send("Please add a question!")
            return
        
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
        resp = random.choice(responses)
    
        # retreives the kirby board template
        with Image.open("resources/kirby_board.jpg") as img:
            draw = ImageDraw.Draw(img)
            
            font = ImageFont.truetype("DejaVuSans.ttf", 20)
            
            # draws the text on the image
            draw.text((90, 25), resp, font=font, fill=(0,0,0))
            
            # saves to memorys
            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            
        await ctx.send(file=discord.File(buf, filename="poyoball.png"))

async def setup(bot):
    await bot.add_cog(PoyoballCog(bot))