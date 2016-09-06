import discord
from discord.ext import commands
from .utils import checks
import random
from haikufinder import HaikuFinder


class Haiku:
    """Haiku commands."""

    def __init__(self, bot):
        self.bot = bot

    async def incoming_messages(self, msg):

        if msg.author.id != self.bot.user.id:
            for haiku in HaikuFinder(msg.content).find_haikus():
                print("!Haiku found in " + str(msg.channel))
                rand_message = random.choice(["Yep, that's a haiku.", "Congratulations! You just made a haiku!", "Wow. This is a beautiful haiku!", "Is that a haiku?", "A wild haiku appears!"])
                message = "{}\n\n`{}\n    {}\n{}`".format(rand_message, haiku[0], haiku[1], haiku[2])
                await self.bot.send_message(msg.channel, message)

    @commands.group(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def haiku(self, ctx):
        """Toggles haiku finder."""
        server = ctx.message.server
        if server.id not in self.settings["SERVER"]:
            self.settings["SERVER"][server.id] = default_settings["SERVER"]["DEFAULT"]
        self.settings["SERVER"][server.id] = not self.settings["SERVER"][server.id]
        if self.settings["SERVER"][server.id]:
            await self.bot.say("Haiku finder enabled!")
        else:
            await self.bot.say("Haiku finder disabled!")
        fileIO("data/haiku/settings.json", "save", self.settings)
				
    @haiku.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    async def addword(self, ctx, word: str, length: int):
        HaikuFinder.add_word(word, length)
        await self.bot.say("Added '{}' : {} to haiku dictionary.".format(word, length))

		
def check_folders():
    if not os.path.exists("data/haiku"):
        print("Creating data/haiku folder...")
        os.makedirs("data/haiku")

def check_files():
    settings_path = "data/haiku/settings.json"

    if not os.path.isfile(settings_path):
        print("Creating default haiku settings.json...")
        fileIO(settings_path, "save", default_settings)
	

def setup(bot):
    check_folders()
    check_files()
    n = Haiku(bot)
    bot.add_cog(n)
    bot.add_listener(n.incoming_messages, "on_message")