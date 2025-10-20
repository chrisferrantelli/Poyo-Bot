import asyncio
import random
import discord
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import aiohttp

from discord.ext import commands

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    """ 
    Poyoball command which acts as a magic 8 ball 
    """
    @commands.command()
    async def poyoball(self, ctx, *, question: str = None):

        if question is None:
            await ctx.send("Please add a question!")
            return
        
        responses = [
                # Positive
                "POYO!",
                "Poyoooo!!",
                "POOYO!",
                "POYOPOYO!!",
                "Poyo~",
                "poyo poyo poyo!",
                "poyo.",
                "POyO!!",

                # Uncertain
                "...poyo?",
                "poy...yo?",
                "poy...",
                "p-p-poyo??",
                "...poyoooooooooo",
                "poyo????"

                # Negative
                "poy-nah.",
                "PO—no.",
                "...noYO.",
                "poyo...",
                "poynope."
        ]
        resp = random.choice(responses)
    
        with Image.open("resources/kirby_board.jpg") as img:
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("DejaVuSans.ttf", 45)
            img_x, img_y = 60,70
            img_width, img_height = 400, 100
            lines = []
            current_line = ""

            for txt in resp.split():
                new_line = current_line + (" " if current_line else " ") + txt
                if draw.textlength(new_line, font=font) <= img_width:
                    current_line = new_line
                else:
                    lines.append(current_line)
                    current_line = txt
                    
            if current_line:
                lines.append(current_line)

            line_height = font.getbbox("A")[3] + 10
            total_text_height = len(lines) * line_height
            y = img_y +(img_height - total_text_height) // 2

            for line in lines:
                line_width = draw.textlength(line, font=font)
                x = img_x + (img_width - line_width) // 2
                draw.text((x,y), line, font=font, fill=(0,0,0,0))
                y += line_height

            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            
        await ctx.send(file=discord.File(buf, filename="poyoball.png"))


    """
    Ego command
    """
    @commands.command()
    async def ego(self, ctx, user: discord.Member= None):
        if user == ctx.author or user == None:
            await ctx.send(f'Your ego is {random.randint(1,100)}%')
        else:
            await ctx.send(f'{user.mention}`s ego is {random.randint(1,100)}%')


    """
    Insult command
    """
    @commands.command()
    async def insult(self, ctx, user: discord.Member = None):
        api_url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                data = await resp.json()
                insultt = data["insult"]
                if resp.status == 200 and (user == ctx.author or user == None):
                    await ctx.send(f'{insultt}')
                else:
                    await ctx.send(f'{user.mention}, {insultt}')


    """
    Hacking command
    """
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


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def botsay(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

async def setup(bot):
     await bot.add_cog(FunCog(bot))