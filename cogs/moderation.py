import discord
import sqlite3
from dotenv import load_dotenv
import os
from discord.ext import commands

class ModerationCog(commands.Cog):
    
    load_dotenv()
    DB_PATH = os.getenv('DB_PATH')

    def __init__(self, bot):
        self.bot = bot

    """
    Whitelist command
    """
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def whitelist(self, ctx, action, *roles: discord.Role):
        conn = sqlite3.connect(os.path.join(self.DB_PATH, "whitelist.db"))
        cursor = conn.cursor()
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS whitelist (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        role_id INTEGER,
                        added_by INTEGER,
                        guild_id INTEGER,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(role_id, guild_id)
                        )
        """)

        if action == "add":
            for role in roles:
                cursor.execute("SELECT 1 FROM whitelist WHERE role_id = ? AND guild_id = ?", (role.id, ctx.guild.id))
                existing_role = cursor.fetchone()
                
                if existing_role == None:
                    cursor.execute("INSERT into whitelist (role_id, added_by, guild_id) VALUES (?, ?, ?)", (role.id, ctx.author.id, ctx.guild.id))
                else:
                    await ctx.send(f"{role.id} is already in the whitelist")
        elif action == "remove":
            for role in roles:
                cursor.execute("DELETE from whitelist WHERE role_id = ?", (role.id,))
        else:
            await ctx.send("Please choose a valid option")
        
        conn.commit()
        conn.close()


    """
    Warn config command
    """
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warnconfig(self, ctx, action, *words):
        conn = sqlite3.connect(os.path.join(self.DB_PATH, "triggerwords.db"))
        cursor = conn.cursor()
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS triggerwords (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        word TEXT NOT NULL,
                        added_by INTEGER,
                        guild_id INTEGER,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        UNIQUE(word, guild_id)
                        )
        """)

        if action == "add_trigger":
            for word in words:
                cursor.execute("SELECT 1 FROM triggerwords WHERE word = ? AND guild_id = ?", (word, ctx.guild.id))
                existing_word = cursor.fetchone()

                if existing_word == None:
                    cursor.execute("INSERT into triggerwords (word, added_by, guild_id) VALUES (?, ?, ?)", (word, ctx.author.id, ctx.guild.id))
                else:
                    await ctx.send(f"{word} already exists as a trigger word")

        elif action == "remove_trigger":
            for word in words:
                cursor.execute("DELETE from triggerwords WHERE word = ?", (word,))
        else:
            await ctx.send("Invalid selection, please try again")

        conn.commit()
        conn.close()


    """
    Listener for automod

    This is where the bot listens for trigger words and punishes accordingly when no one is available
    """
    @commands.Cog.listener()
    async def on_message(self, message):
        conn = sqlite3.connect(os.path.join(self.DB_PATH, "triggerwords.db"))
        cursor = conn.cursor()
        cursor.execute("SELECT word FROM triggerwords WHERE guild_id = ?", (message.guild.id,))
        user_words = cursor.fetchall()       
        conn.close()
        
        conn = sqlite3.connect(os.path.join(self.DB_PATH, "whitelist.db"))
        cursor = conn.cursor()
        cursor.execute("SELECT role_id FROM whitelist WHERE guild_id = ?", (message.guild.id,))
        whitelisted_rows = cursor.fetchall()
        conn.close()

        whitelisted_roles = [whitelisted_row[0] for whitelisted_row in whitelisted_rows]

        for role in message.author.roles:
            if role.id in whitelisted_roles:
                return

        if message.author == self.bot.user:
            return
        
        for user_word in user_words:
            word = user_word[0]

            if word in message.content.lower():
                reason = f"Used trigger word: {word}"
                conn = sqlite3.connect(os.path.join(self.DB_PATH, "userwarnings.db", timeout = 10))
                cursor = conn.cursor()
                cursor.execute("SELECT warn_count FROM userwarnings WHERE user_id = ? AND guild_id = ?", (message.author.id, message.guild.id))
                user_words = cursor.fetchone()

                if user_words:
                    cursor.execute("UPDATE userwarnings SET warn_count = warn_count + 1 WHERE user_id = ? AND guild_id = ?", (message.author.id, message.guild.id))
                else:
                    cursor.execute("INSERT INTO userwarnings (user_id, reason, guild_id, warn_count) VALUES (?, ?, ?, 1)", (message.author.id, reason, message.guild.id))

                conn.commit()

                cursor.execute("SELECT warn_count from userwarnings WHERE user_id = ? AND guild_id = ?", (message.author.id, message.guild.id))
                warn_count = cursor.fetchone()[0]
                conn.close()    

                if warn_count == 4:
                    print("You exceed the threshold")
                    try:
                        await message.author.kick(reason = f"⚠️{message.author.mention} has exceeded max warns!")
                        embed = discord.Embed(
                        color = self.bot.embed_color,
                        title ="Kick Notice",
                        description=f"🥾 {message.author.mention} has been kicked for being warned {warn_count} times."
                    )
                        embed.add_field(name = "Reason", value = reason)
                        await message.channel.send(embed = embed)
                    except discord.HTTPException as err:
                        await message.channel.send(f"An error occurred while trying to kick {message.author.mention}: {err}")
                elif warn_count >= 5:
                    try:
                        await message.author.ban(reason = f"⚠️ {message.author.mention} has excceeded max warns!")
                        embed = discord.Embed(
                        color = discord.Color.red,
                        title ="Ban Notice",
                        description=f"🚫 {message.author.mention} has been banned for being warned {warn_count} times."
                    )
                        embed.add_field(name = "Reason", value = reason)
                        await message.channel.send(embed = embed)
                    except discord.HTTPException as err:
                        await message.channel.send(f"An error occurred while trying to ban {message.author.mention}: {err}")
            await self.bot.process_commands(message)


    """
    Warn user command
    """
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def warnuser(self, ctx, member: discord.Member, *, reason="No reason provided"):
        if ctx.author.top_role < member.top_role:
            embed = discord.Embed(
                    color = self.bot.embed_color,
                    title =  "User Info",
                    description = "You dare try to warn a higher being mortal?"
            )
            await ctx.send(embed=embed)
        elif ctx.author.top_role > member.top_role:
            author = ctx.author
            embed2 = discord.Embed(
                    color = self.bot.embed_color,
                    title = "User Info",
                    description = f"The user {member.mention} has been **warned!**"
            )               
            embed2.add_field(name = f"Staff", value = f"{author}")
            embed2.add_field(name = f"You were warned for: ", value = f"{reason}")
            await ctx.send(embed=embed2)
            
        conn = sqlite3.connect("userwarnings.db")
        cursor = conn.cursor()
        cursor.execute("""
                        CREATE TABLE IF NOT EXISTS userwarnings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        reason TEXT,
                        guild_id INTEGER,
                        warn_count INTEGER,x
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
        """)

        cursor.execute("SELECT COUNT (*) FROM userwarnings WHERE user_id = ? and guild_id = ?", (member.id, ctx.guild.id))
        user_exist = cursor.fetchone()[0]

        if user_exist:
            cursor.execute("UPDATE userwarnings SET warn_count = warn_count + 1 WHERE user_id = ? AND guild_id = ?", (member.id, ctx.guild.id))
        else:
            cursor.execute("INSERT INTO userwarnings (user_id, reason, guild_id, warn_count) VALUES (?, ?, ?, 1)", (member.id, reason, ctx.guild.id))

        cursor.execute("SELECT warn_count FROM userwarnings WHERE user_id = ? AND guild_id = ?", (member.id, ctx.guild.id))
        warn_count = cursor.fetchone()[0]
        conn.commit()
        conn.close()

        if warn_count == 4:
            print("You exceed the threshold")
            try:
                await member.kick(reason = f"⚠️{member.mention} has exceeded max warns!")
                embed = discord.Embed(
                color = self.bot.embed_color,
                title ="Kick Notice",
                description=f"🥾 {member.mention} has been kicked for being warned {warn_count} times."
            )
                embed.add_field(name = "Reason", value = reason)
                await ctx.send(embed = embed)
            except discord.HTTPException as err:
                await ctx.send(f"An error occurred while trying to kick {member.mention}: {err}")
        elif warn_count >= 5:
            try:
                await member.ban(reason = f"⚠️ {member.mention} has excceeded max warns!")
                embed = discord.Embed(
                color = discord.Color.red,
                title ="Ban Notice",
                description=f"🚫 {member.mention} has been banned for being warned {warn_count} times."
            )
                embed.add_field(name="Reason", value=reason)
                await ctx.send(embed=embed)
            except discord.HTTPException as err:
                await ctx.send(f"An error occurred while trying to ban {member.mention}: {err}")

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))