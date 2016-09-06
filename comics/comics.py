import discord
from discord.ext import commands
import random
import aiohttp
from .utils import checks
from bs4 import BeautifulSoup

class Comics:
    """Comics commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    @checks.mod_or_permissions(manage_server=True)
    async def comics(self, ctx):
        """Sends comics."""
        if ctx.invoked_subcommand is None:
            await self.bot.say("Type help comics for info.")

    @comics.command(pass_context=True, no_pm=True)
    async def asp(self, ctx):
        try:
            page = await aiohttp.get('http://www.amazingsuperpowers.com/?randomcomic&nocache=1')
            page = await page.text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="comic-1").find("img").get("src")
            await self.bot.say(image)
        except Exception as e:
            await self.bot.say(':x: Error: ' + str(e))

    @comics.command(pass_context=True, no_pm=True)
    async def rcg(self, ctx):
        """explosm random comic generator"""
        try:
            page = await aiohttp.get('http://explosm.net/rcg')
            page = await page.text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="rcg-comic").get('src').replace("//", "http://")
            await self.bot.say(image)
        except Exception as e:
            await self.bot.say(':x: Error: ' + str(e))

    @comics.command(pass_context=True, no_pm=True, hidden=True)
    async def acomics(self, ctx, name):
        """acomics.ru comics"""
        try:
            page = await aiohttp.get('http://acomics.ru/' + name)
            page = await page.text()
            soup = BeautifulSoup(page, 'html.parser')
            total = soup.find("a", "read2").get("href")[len(name)+2:]
            rand_num = random.randint(1, int(total))
            page = await aiohttp.get('http://acomics.ru/' + name + "/" + str(rand_num))
            page = await page.text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="mainImage").get("src")
            await self.bot.say('http://acomics.ru' + image)
        except Exception as e:
            await self.bot.say(':x: Error: ' + str(e))

    @comics.command(pass_context=True, no_pm=True)
    async def smbc(self, ctx):
        """smbc comics"""
        try:
            page = await aiohttp.get('http://www.smbc-comics.com/')
            page = await page.text()
            soup = BeautifulSoup(page, 'html.parser')
            link = soup.find("a", "random").get('href')
            page = await aiohttp.get('http://www.smbc-comics.com/' + link)
            page = await page.text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="comic").get('src')
            await self.bot.say("http://www.smbc-comics.com/" + image)
        except Exception as e:
            await self.bot.say(':x: Error: ' + str(e))

    @comics.command(pass_context=True, no_pm=True)
    async def nerfnow(self, ctx):
        """smbc comics"""
        try:
            page = await aiohttp.get('http://www.nerfnow.com/')
            page = await page.text()
            soup = BeautifulSoup(page, 'html.parser')
            soup = soup.find(id="comments_link").find("a").get("href")
            link = soup[:-9]
            total = int(link.split("comic/")[1])
            rand = random.randint(1, total)
            page = await aiohttp.get("http://www.nerfnow.com/comic/" + str(rand))
            page = await page.text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="comic").find("img").get("src")
            await self.bot.say(image)
        except Exception as e:
            await self.bot.say(':x: Error: ' + str(e))

    @comics.command(pass_context=True, no_pm=True)
    async def cah(self, ctx):
        """cah comics"""
        try:
            page = await aiohttp.get('http://explosm.net/comics/random/')
            page = await page.text()
            soup = BeautifulSoup(page, 'html.parser')
            image = soup.find(id="main-comic").get('src')
            await self.bot.say("http:" + image)
        except Exception as e:
            await self.bot.say(':x: Error: ' + str(e))

def setup(bot):
    n = Comics(bot)
    bot.add_cog(n)