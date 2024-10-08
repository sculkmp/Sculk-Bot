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
from discord import app_commands
from datetime import datetime, timedelta

import modules.log as log

import json; data = json.load(open('config.json', 'r', encoding='utf-8'))

class UnmuteCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.checks.has_any_role(*data['roles']['admin'])
    @app_commands.command(name='unmute', description='Unmute a member')
    async def unmute(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer(ephemeral=False)
        try:
            await member.timeout(None)
            embed = discord.Embed(description=f'### {member.mention} has been unmuted', colour=0x28b4d8)
            await interaction.channel.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(description='### An error occurred', colour=0x28b4d8)
            await interaction.followup.send(embed=embed, ephemeral=True)
            log.write('cogs.commands.unmute', e, log.levels.error)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UnmuteCog(bot))