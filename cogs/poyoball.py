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

                # Negative
                "poy-nah.",
                "PO—no.",
                "...noYO.",
                "poyo...",
                "poynope."
        ]
        resp = random.choice(responses)
    
        # retreives the kirby board template
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

async def setup(bot):
    await bot.add_cog(PoyoballCog(bot))