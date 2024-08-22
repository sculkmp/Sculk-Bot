#    ____             _ _              __  __ ____
#   / ___|  ___ _   _| | | __         |  \/  |  _ \
#   \___ \ / __| | | | | |/ /  _____  | |\/| | |_) |
#    ___) | (__| |_| | |   <  |_____| | |  | |  __/
#   |____/ \___|\__,_|_|_|\_\         |_|  |_|_|
# 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  @author: SculkTeams
#  @link: http://www.sculkmp.org/

import discord
from discord.ext import commands
import asyncio
import re
import datetime

class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        link_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        for url in re.findall(link_regex, message.content):
            if not url.startswith('https://github.com/sculk'):
                await self.timeout(message.author, message.guild, "30m")
                await message.delete()
                embed = discord.Embed(title="Mute", description=f"{message.author.mention} was silenced for 10 minutes for posting an unauthorized link!", color=0xff0000)
                await message.channel.send(embed=embed)

    async def timeout(self, member, guild, duration):
        duration_in_seconds = self.parse_duration(duration)
        until = discord.utils.utcnow() + datetime.timedelta(seconds=duration_in_seconds)
        await member.timeout(until, reason="Link not allowed")
        async def unmute_task():
            await asyncio.sleep(duration_in_seconds)
            await member.timeout(None, reason="End of timeout")

        asyncio.create_task(unmute_task())

    def parse_duration(self, duration):
        duration = duration.lower()
        if duration.endswith("s"):
            return int(duration[:-1])
        elif duration.endswith("m"):
            return int(duration[:-1]) * 60
        elif duration.endswith("h"):
            return int(duration[:-1]) * 3600
        else:
            raise ValueError("Invalid duration format")

async def setup(bot):
    await bot.add_cog(Automod(bot))