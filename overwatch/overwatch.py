import discord
from discord.ext import commands
import aiohttp
import traceback
import json
from __main__ import send_cmd_help

#This cog may be broken.

#Overwatch REST API
#https://api.watcher.gg

# * /players/search/name/ - Search for players

# * /players/{platform}/{region}/{name}/refresh/ - Refresh player profile. If used together with user search: Adds user profile to database, if profile data is missing.

# * /players/{platform}/{region}/{name}/ - Get user profile data

# * /players/{platform}/{region}/{name}/hero-stats?hero={hero} - Get stats of the chosen hero tracked over several days (-1 == total stats)

# * /gamedata/heroes - Get static list of hero id's and name's.

# * /heroes?platform={platform} - Get hero kda, win rate, time played per platform

# * /leaderboards/{stat}/{hero}/{mode}/{platform}?page={page}/ - Get paged leaderboards.

# * /leaderboards/search/{stat}/{hero}/{mode}/{platform}/{name}/ - Get user position in the leaderboard.

#Correct values for {stat} field: kda, average_damage_done, average_eliminations, average_healing, average_score, most_game_damage_done, most_game_damage_done, most_game_eliminations, most_game_healing_done, medals, games_won, games_played, time_played
#Correct values for {mode} field: 0

class Overwatch:
    """Overwatch commands."""

    def __init__(self, bot):
        self.bot = bot
        self.cookies = None
        self.servers = ["pc", "psn", "xbl"]
        self.regions = ["us", "eu", "kr"]
        self.headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Host": "api.watcher.gg", "Connection": "Keep-Alive", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"}

    @commands.group(pass_context=True)
    async def overwatch(self, ctx):
        """Overwatch Commands"""
        if ctx.invoked_subcommand is None or \
                isinstance(ctx.invoked_subcommand, commands.Group):
            #await self.bot.say("Correct servers are: `pc, psn, xbl`...")
            await send_cmd_help(ctx)

    @overwatch.command(pass_context=True, no_pm=False, hidden=True)
    async def refresh(self, ctx, server: str, region: str, bnid: str):
        """Refreshes Overwatch profile"""
        refreshurl = ("https://api.watcher.gg/players/{}/{}/{}/refresh".format(server, region, bnid.replace("#", "%23").replace(" ", "%20")))
        resp = await aiohttp.request('GET', refreshurl, headers=self.headers)
        print(resp.status)
        resp.close()

    @overwatch.command(pass_context=True, no_pm=False, hidden=True)
    async def search(self, ctx, bnid: str):
        """Search Overwatch profiles"""
        searchurl = ("https://api.watcher.gg/players/search/{}".format(bnid.replace("#", "%23")))
        resp = await aiohttp.request('GET', searchurl, headers=self.headers)
        print(resp.status)
        resp.close()

    #https://api.watcher.gg/players/search/{}
    @overwatch.group(pass_context=True, no_pm=False)
    async def update(self, ctx):
        """Requests profile update"""
        if ctx.invoked_subcommand is None or isinstance(ctx.invoked_subcommand, commands.Group):
                    await send_cmd_help(ctx)

    @update.command(name="pc", pass_context=True, no_pm=False)
    async def update_pc(self, ctx, region: str, battletag: str):
        searchurl = ("https://api.watcher.gg/players/search/{}".format(battletag.replace("#", "%23")))
        refreshurl = ("https://api.watcher.gg/players/{}/{}/{}/refresh".format(region, battletag.replace("#", "%23")))
        resp = await aiohttp.request('GET', searchurl, headers=self.headers)
        if resp.status == 200:
            print("search", resp.status)
            resp.close()
            resp = await aiohttp.request('GET', refreshurl, headers=self.headers)
            if resp.status == 200:
                print("refresh", resp.status)
                resp.close()
                await self.bot.say("Done! Try `profile pc <region> <battletag>` command now!")
            else:
                resp.close()
                await self.bot.say("Failed to update profile.")
        else:
            resp.close()
            await self.bot.say("This player probably does not exist.")

    @update.command(name="psn", pass_context=True, no_pm=False)
    async def update_psn(self, ctx, psnid: str):
        """Check Playstation Network Overwatch profile stats"""
        searchurl = ("https://api.watcher.gg/players/search/{}".format(psnid.replace("#", "%23")))
        refreshurl = ("https://api.watcher.gg/players/psn/global/{}/refresh".format(psnid.replace("#", "%23")))
        resp = await aiohttp.request('GET', searchurl, headers=self.headers)
        if resp.status == 200:
            print("search", resp.status)
            resp.close()
            resp = await aiohttp.request('GET', refreshurl, headers=self.headers)
            if resp.status == 200:
                print("refresh", resp.status)
                resp.close()
                await self.bot.say("Done! Try `profile psn <psnid>` command now!")
            else:
                resp.close()
                await self.bot.say("Failed to update profile.")
        else:
            resp.close()
            await self.bot.say("This player probably does not exist.")

    @update.command(name="xbl", pass_context=True, no_pm=False)
    async def update_xbl(self, ctx, *, gamertag: str):
        """Check Xbox Live Overwatch profile stats"""
        searchurl = ("https://api.watcher.gg/players/search/{}".format(gamertag.replace("#", "%23")))
        refreshurl = ("https://api.watcher.gg/players/xbl/global/{}/refresh".format(gamertag.replace("#", "%23")))
        resp = await aiohttp.request('GET', searchurl, headers=self.headers)
        if resp.status == 200:
            print("search", resp.status)
            resp.close()
            resp = await aiohttp.request('GET', refreshurl, headers=self.headers)
            if resp.status == 200:
                print("refresh", resp.status)
                resp.close()
                await self.bot.say("Done! Try `profile xbl <gamertag>` command now!")
            else:
                resp.close()
                await self.bot.say("Failed to update profile.")
        else:
            resp.close()
            await self.bot.say("This player probably does not exist.")

    @overwatch.group(pass_context=True, no_pm=False)
    async def profile(self, ctx):
        """Check Overwatch profile stats"""
        if ctx.invoked_subcommand is None or \
                isinstance(ctx.invoked_subcommand, commands.Group):
            #await self.bot.say("Correct servers are: `pc, psn, xbl`...")
            await send_cmd_help(ctx)

    @profile.command(name="pc", pass_context=True, no_pm=False)
    async def profile_pc(self, ctx, region: str, battletag: str):
        """Check PC Overwatch profile stats"""
        try:
            if region not in self.regions:
                await self.bot.say("Correct regions are: `us, eu, kr`...")
                return
            profileurl = ("https://api.watcher.gg/players/pc/{}/{}".format(region, battletag.replace("#", "%23")))
            resp = await aiohttp.request('GET', profileurl, headers=self.headers)
            if resp.status == 404:
                resp.close()
                await self.bot.say("Sorry, that player was never updated or does not exist! You may need to use `update pc <region> <battletag>` command first.")
                return
            if resp.status == 200:
                resp = await resp.text()
                data = json.loads(resp)
                msg = self.profile_message(data, "pc", region, battletag)
                await self.bot.say(msg)
            else:
                await self.bot.say("Error.")
        except:
            print(traceback.format_exc())

    @profile.command(name="psn", pass_context=True, no_pm=False)
    async def profile_psn(self, ctx, psnid: str):
        """Check PSN Overwatch profile stats"""
        try:
            profileurl = ("https://api.watcher.gg/players/psn/global/{}".format(psnid.replace("#", "%23")))
            resp = await aiohttp.request('GET', profileurl, headers=self.headers)
            if resp.status == 404:
                resp.close()
                await self.bot.say("Sorry, that player was never updated or does not exist! You may need to use `update psn <psnid>` command first.")
                return
            if resp.status == 200:
                resp = await resp.text()
                data = json.loads(resp)
                msg = self.profile_message(data, "psn", "global", psnid)
                await self.bot.say(msg)
            else:
                await self.bot.say("Error.")
        except:
            print(traceback.format_exc())

    @profile.command(name="xbl", pass_context=True, no_pm=False)
    async def profile_xbl(self, ctx, *, gamertag: str):
        """Check XBL Overwatch profile stats"""
        try:
            profileurl = ("https://api.watcher.gg/players/xbl/global/{}".format(gamertag.replace("#", "%23")))
            resp = await aiohttp.request('GET', profileurl, headers=self.headers)
            if resp.status == 404:
                resp.close()
                await self.bot.say("Sorry, that player was never updated or does not exist! You may need to use `update xbl <gamertag>` command first.")
                return
            if resp.status == 200:
                resp = await resp.text()
                data = json.loads(resp)
                msg = self.profile_message(data, "xbl", "global", gamertag)
                await self.bot.say(msg)
            else:
                await self.bot.say("Error.")
        except:
            print(traceback.format_exc())

    def profile_message(self, data, server, region, identifier):
        portrait = "https://static.watcher.gg/portraits/{}.png".format(data["data"]["player"]["portrait"])
        level = data["data"]["player"]["level"]
        winrate = data["data"]["heroStats"][0]["gamesWon"] / data["data"]["heroStats"][0]["gamesPlayed"] * 100
        games_played = data["data"]["heroStats"][0]["gamesPlayed"]
        score = data["data"]["heroStats"][0]["score"]
        kda = data["data"]["heroStats"][0]["kda"]
        time_played_seconds = data["data"]["heroStats"][0]["timePlayed"]
        time_played_minutes = time_played_seconds / 60
        time_played_hours = time_played_seconds / 3600
        gold_medals = data["data"]["heroStats"][0]["medalsGold"]
        silver_medals = data["data"]["heroStats"][0]["medalsSilver"]
        bronze_medals = data["data"]["heroStats"][0]["medalsBronze"]
        total_medals = gold_medals + silver_medals + bronze_medals
        damage_done = data["data"]["heroStats"][0]["damageDone"]
        damage_per_sec = damage_done / time_played_seconds
        healing_done = data["data"]["heroStats"][0]["healingDone"]
        healing_per_sec = healing_done / time_played_seconds
        eliminations = data["data"]["heroStats"][0]["eliminations"]
        eliminations_per_min = eliminations / time_played_minutes
        multi_kills = data["data"]["heroStats"][0]["multiKills"]
        objective_kills = data["data"]["heroStats"][0]["objectiveKills"]
        achieve_points_total = 0
        for a in data["data"]["achievements"]:
            achieve_points_total += a["points"]
        games_won = data["data"]["heroStats"][0]["gamesWon"]
        games_lost = games_won - games_played
        msg = ("Stats for {}-{} <**{}**>:\nProfile image: {}\nLevel: **{}**\nWin Rate: **{}** ({} / {})\nScore: **{}**\nKDA: **{}**\nTime Played: **{}** hours\nTotal Medals: **{}** (Gold: {} Silver: {} Bronze: {})\nDamage Dealt: **{}** ({} / sec)\nHealing Done: **{}** ({} / sec)\nEliminations: **{}** ({} / min)\nMulti-Kills: **{}**\nObjective Kills: **{}**\nAchievement points: **{}**".format(server, region, identifier, portrait, level, round(winrate, 2), games_won, games_lost, score, round(kda, 2), time_played_hours, total_medals, gold_medals, silver_medals, bronze_medals, damage_done, round(damage_per_sec, 2), healing_done, round(healing_per_sec, 2), eliminations, round(eliminations_per_min, 2), multi_kills, objective_kills, achieve_points_total))
        return msg
		#;_;

def setup(bot):
    n = Overwatch(bot)
    bot.add_cog(n)