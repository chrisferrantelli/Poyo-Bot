from discord.ext import commands
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

class TldrCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_fusions = {}

    @commands.command()
    async def tldr(self,ctx):
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
                max_length=80,
                min_length=20,
                do_sample=False
            )

            tldr = summary[0]['summary_text']
            await ctx.send(f"Here is the tldr: {tldr}")
            
        except Exception as err:
            await ctx.send(f"There was an error: {err}")
            return

async def setup(bot):
    await bot.add_cog(TldrCog(bot))
