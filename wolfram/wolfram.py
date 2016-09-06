import discord
from discord.ext import commands
from .utils import checks
from .utils.dataIO import fileIO
import wolframalpha
import os
import asyncio

class Wolfram:
    """Wolfram commands."""

    def __init__(self, bot):
        self.bot = bot
        self.settings = fileIO("data/wolfram/settings.json", "load")
        self.wolfram_client = wolframalpha.Client(self.settings["WOLFRAM_CLIENT_ID"])

    @commands.command(pass_context=True, no_pm=True)
    async def wolfram(self, ctx, *, query: str):
        """Ask wolfram anything"""
        try:
            res = self.wolfram_client.query(query)
            if len(res.pods) != 0:
                i = 0
                msgs = [""]
                for pod in res.pods:
                    data = "**{}:**\n".format(str(pod.title))
                    if str(pod.text) == "None":
                        data += "`{}`\n".format(str(pod.img))
                    else:
                        data +=  "`{}`\n".format(str(pod.text))
                    if len(msgs[i]) + 5 > 2000:
                        i += 1
                        msgs.append("{}\n".format(data))
                    else:
                        msgs[i] += "{}\n".format(data)
                for msg in msgs:
                    await self.bot.say(msg)
                    await asyncio.sleep(1)
            else:
                await self.bot.say(":x: Can't calculate this.")
        except:
            self.bot.say(":x: Error.")

    @commands.command(no_pm=False)
    @checks.is_owner()
    async def wolframset(self, ID: str=None):
        """Sets the Wolfram Client ID"""
        self.settings["WOLFRAM_CLIENT_ID"] = ID
        fileIO("data/wolfram/settings.json", "save", self.settings)
        if not ID:
            await self.bot.say("Wolfram has been disabled")
        else:
            await self.bot.say("Wolfram Client ID has been set")

def check_folders():
    if not os.path.exists("data/wolfram"):
        print("Creating data/wolfram folder...")
        os.makedirs("data/wolfram")

def check_configs():
    settings = {"WOLFRAM_CLIENT_ID" : None}

    if not os.path.isfile('data/wolfram/settings.json'):
        fileIO("data/wolfram/settings.json", "save", settings)

def setup(bot):
    check_folders()
    check_configs()
    n = Wolfram(bot)
    bot.add_cog(n)