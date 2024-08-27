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

import json; data = json.load(open('config.json', 'r', encoding='utf-8'))
import modules.log as log
import asyncio

class autojoin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        autorole = member.guild.get_role(data['autorole'])
        if autorole is None:
            log.write('cogs.events.autorole', f'Could not find autorole with id {data["autorole"]} in guild {member.guild.name}', log.levels.error)
            return
        await member.add_roles([autorole])
        log.write('cogs.events.autorole', f'{member} joined the server and was given the autorole role', log.levels.debug)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        for guild in self.bot.guilds:
            autorole = guild.get_role(data['autorole'])
            if autorole is None:
                log.write('cogs.events.autorole', f'Could not find autorole with id {data["autorole"]} in guild {guild.name}', log.levels.error)
                continue
            for member in guild.members:
                if member.bot:
                    break
                if autorole not in member.roles:
                    await member.add_roles([autorole])
                    log.write('cogs.events.autorole', f'{member} received the autorole role because he did not possess it', log.levels.debug)
                    await asyncio.sleep(0.5)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(autojoin(bot))