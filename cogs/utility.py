from discord.ext import commands
import discord
from transformers import pipeline
import random
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.stem import WordNetLemmatizer


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
        elif action == "genzz":
            slang = {
                "hello": ["yo", "hey bestie", "sup"],
                "yes": ["fr", "deadass", "on god"],
                "no": ["nah frfr", "💀"],
                "good": ["fire", "that slaps", "bussin"],
                "cool": ["cold af", "lit", "goated", "hard"],
                "bad": ["mid", "trash", "not it chief"],
                "funny": ["i’m screaming", "💀💀💀", "i can’t rn"],
                "amazing": ["insane", "crazy fr", "wild"],
                "true": ["no cap"],
                "you": ["bestie", "fam", "bruh"],
                "i": ["ya boy", "ion"],
                "know": ["ya kno what I'm sayin?"],
                "friend": ["bestie", "homie", "brokie", "my slime"],
                "angry": ["pressed", "mad mad", "salty", "heated"],
                "happy": ["vibin", "feelin myself", "big chillin"],
                "sad": ["lowkey cryin", "in my feels", "down bad"],
                "tired": ["dead inside", "exhausted af", "need a nap fr"],
                "money": ["bread", "bag", "racks", "shmoney"],
                "eat": ["munch", "devour", "inhale that"],
                "run": ["dip", "skedaddle", "yeet myself out"],
                "crazy": ["wildin", "off the rails", "unhinged"],
                "beautiful": ["a whole meal", "looking valid", "10/10 no notes"],
                "ugly": ["built like a minecraft mob", "yikes", "not the move"],
                "love": ["simp for", "got me weak for", "obsessed with"],
                "hate": ["can’t stand", "done with", "ick"],
                "fast": ["zoomin", "speedrun that", "quick af"],
                "slow": ["laggin", "on 1 fps", "movin like dial-up"],
                "laugh": ["LMFAOO", "cryin", "💀💀💀💀💀"],
                "sleep": ["knocked", "out cold", "brb entering sleep mode"],
                "fight": ["throw hands", "square up", "run the fade", "run fades", "scrap up"],
                "strong": ["built different", "swole", "alpha energy", "goated with the sauce"],
                "weak": ["baby girl behavior", "flimsy", "soft launchin my Ls"],
                "smart": ["big brain", "galaxy brain", "IQ 9000"],
                "stupid": ["NPC", "smooth brain", "brain.exe stopped working"],
                "awesome": ["gas", "peak", "W fr"],
                "boring": ["dry af", "snoozefest", "L take"],
                "excited": ["amped", "turnt", "hyped up"],
                "scared": ["spooked", "shook", "heart doing parkour"],
                "goodbye": ["ight imma head out", "peace out bestie", "deuces"],
                "power": ["energy", "aura", "ki levels", "vibes"],
                "train": ["grind", "hit the dojo", "level up"],
                "meditate": ["zone out", "get centered", "mental reset"],
                "focus": ["lock in", "dial in", "zero in"],
                "calm": ["chill af", "unbothered", "zen mode"],
                "respect": ["props", "mad love", "W energy"],
                "earned": ["deserved", "no handouts", "put in work", "grinded for it", "came up legit", "worked for that W"],
                "evil": ["villain vibes", "menace arc", "off the shits"],
                "growth": ["glow-up", "character dev", "level-up"],
                "mentor": ["sensei", "coach fr", "life guru"],
                "father": ["pops", "OG", "real one"],
                "real": ["frfr", "no cap", "authentic"],
                "heart": ["core", "soul", "spirit"],
                "soul": ["essence", "vibe", "inner fire"],
                "discipline": ["grindset", "main character focus", "locked-in energy"],
                "silent": ["lowkey", "quiet flex", "stealth mode"],
                "powerful": ["bussin", "top-tier", "god-tier"],
                "humble": ["lowkey flex", "quiet king", "unbothered legend"]
            }

            lemmatizer = WordNetLemmatizer()
            result = []
            
            for word in quoted_result.lower().split():
                clean_word = word.strip("?.!,")

                lemma_vrb = lemmatizer.lemmatize(clean_word, pos="v")
                lemma_adj = lemmatizer.lemmatize(clean_word, pos="a")
                base_lemma = lemma_vrb if lemma_vrb in slang else lemma_adj if lemma_adj in slang else clean_word
                if base_lemma in slang:
                    word = random.choice(slang[base_lemma])
                result.append(word)
            genz_embed = discord.Embed(
                color = self.bot.embed_color,
                description = ' '.join(result)
            )
            genz_embed.set_footer(text = f"- {quoted_user.display_name}")
            await ctx.send(embed = genz_embed)

async def setup(bot):
    await bot.add_cog(UtilityCog(bot))