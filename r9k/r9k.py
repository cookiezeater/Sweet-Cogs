import discord
from discord.ext import commands
import __main__
import os
import sqlite3
import re
from .utils import checks
from .utils.dataIO import fileIO

main_path = os.path.dirname(os.path.realpath(__main__.__file__))

default_settings = {"SERVER": {"DEFAULT": False}}

class R9k:
    """R9k commands."""

    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('data/r9k/messages.db')
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS messages (message TEXT)")
        self.settings = fileIO("data/lolz/settings.json", "load")

    @commands.group(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def r9k(self, ctx):
        """Toggles r9k mode."""
        server = ctx.message.server
        if server.id not in self.settings["SERVER"]:
            self.settings["SERVER"][server.id] = default_settings["SERVER"]["DEFAULT"]
        self.settings["SERVER"][server.id] = not self.settings["SERVER"][server.id]
        if self.settings["SERVER"][server.id]:
            await self.bot.say("R9K mode enabled!")
        else:
            await self.bot.say("R9K mode disabled!")
        fileIO("data/r9k/settings.json", "save", self.settings)
		
    @r9k.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def reset(self, ctx):
        """Resets the database."""
        self.c.execute("DROP TABLE 'messages'")
        self.c.execute("CREATE TABLE messages (message TEXT)")
        self.conn.commit()
        await self.bot.say("(╯°□°）╯︵ ┻━┻ DROP TABLE 'messages'")

    async def incoming_messages(self, msg):
        if self.settings["SERVER"].get(msg.server.id, False):
            if msg.author.id != self.bot.user.id:
                if msg.content != "":
                    message = msg.content.lower().replace("'", "''")
                    message = re.sub(r"\<\@\d*\>", '', message) #remove mentions
                    #print(message)
                    message = re.sub(r"(?<!\w)-+|-+(?!\w)", '', message) #remove lone dashes
                    #print(message)
                    message = re.sub(r"[^а-яА-Яa-zA-Z\d -]+", '', message) #remove punctuation, also support for russian symbols
                    #print(message)
                    message = re.sub(r"\s+", '', message) #remove all whitespace
                    #print(message)
                    self.c.execute("SELECT * FROM messages WHERE message = '{}'".format(message))
                    match = self.c.fetchone()
                    if match is None:
                        #print("added string")
                        self.c.execute("INSERT INTO messages VALUES ('{}')".format(message))
                        self.conn.commit()
                        print(message)
                    else:
                        #print("matched string")
                        await self.bot.send_message(msg.channel, "deleting message: " + msg.id)
                        await self.bot.delete_message(msg)
                        print(message)

def check_folders():
    if not os.path.exists("data/r9k"):
        print("Creating data/r9k folder...")
        os.makedirs("data/r9k")

def check_files():
    settings_path = "data/r9k/settings.json"

    if not os.path.isfile(settings_path):
        print("Creating default r9k settings.json...")
        fileIO(settings_path, "save", default_settings)

def setup(bot):
    check_folders()
    check_files()
    n = R9k(bot)
    bot.add_listener(n.incoming_messages, "on_message")
    bot.add_cog(n)