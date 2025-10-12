from discord.ext import commands
import discord
from transformers import pipeline
import random

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_fusions = {}


    """
    Tldr command
    """
    @commands.command()
    async def tldr(self, ctx):
        if not ctx.message.reference:
            await ctx.send("Please reply to a long message with !tldr")
            return

        ref_msg = await ctx.fetch_message(ctx.message.reference.message_id)
        result = ref_msg.content

        if not result and len(result) < 50:
            await ctx.send("This message is too short")
            return
        try:
            summary = summarizer(
                result,
                max_length=100,
                min_length=40,
                do_sample=False
            )
            tldr = summary[0]['summary_text']
            await ctx.send(f"Here is the tldr: {tldr}")
        except Exception as err:
            await ctx.send(f"There was an error trying to summarize the message: {err}")
            return
        

    """
    Quote command
    """
    @commands.command()
    async def quote(self, ctx, action: str = ""):
        if not ctx.message.reference:
            await ctx.send("Must reply !quote <optional: action> to a users message")
            return
    
        ref_msg = await ctx.fetch_message(ctx.message.reference.message_id)
        quoted_user = ref_msg.author
        quoted_result = ref_msg.content
        new_result = ""

        if action == "":
            normal_embed = discord.Embed(
                color = self.bot.embed_color,
                description = f"'{quoted_result}'"
            )
            normal_embed.set_footer(text = f"- {quoted_user.display_name}")
            await ctx.send(embed = normal_embed)
            return
        elif action == "sarcastic":
            for text in range(len(quoted_result)):
                if text % 2 == 0:
                    new_result += quoted_result[text].lower()
                else:
                    new_result += quoted_result[text].upper()
            sarcastic_embed = discord.Embed(
                color = self.bot.embed_color,
                description = f"'{new_result}'"
            )
            sarcastic_embed.set_footer(text = f"- {quoted_user.display_name}")
            await ctx.send(embed = sarcastic_embed)
        elif action == "valley-girl":
            fillers = ["like", "literally", "omg", "totally", "you know", "like ummmm", "ummmmm"]
            result = []
            for word in quoted_result.lower().split():
                result.append(word)
                if random.random() < 0.3:
                    result.append(random.choice(fillers))
            valleygirl_embed = discord.Embed(
                color = self.bot.embed_color,
                description = ' '.join(result)
            )
            valleygirl_embed.set_footer(text = f"- {quoted_user.display_name}")
            await ctx.send(embed = valleygirl_embed) 
        elif action == "genz":
            slang = {
                "hello": ["yo", "hey bestie", "sup"],
                "yes": ["fr", "deadass", "on god"],
                "no": ["nah frfr", "💀"],
                "good": [ "fire", "that slaps", "bussin"],
                "cool": ["cold af", "lit", "goated"],
                "bad": ["mid", "trash", "not it chief"],
                "funny": ["i’m screaming", "💀💀💀", "i can’t rn"],
                "amazing": ["insane", "crazy fr", "wild"],
                "true": ["no cap"],
                "you": ["bestie", "fam", "bruh"],
                "i": ["ya boy", "ion"],
                "know": ["ya kno what I'm sayin?"]
            }
            result = []
            for word in quoted_result.lower().split():
                clean_word = word.strip("?.!,")
                if clean_word in slang:
                    word = random.choice(slang[clean_word])
                result.append(word)
            genz_embed = discord.Embed(
                color = self.bot.embed_color,
                description = ' '.join(result)
            )
            genz_embed.set_footer(text = f"- {quoted_user.display_name}")
            await ctx.send(embed = genz_embed)

async def setup(bot):
    await bot.add_cog(UtilityCog(bot))