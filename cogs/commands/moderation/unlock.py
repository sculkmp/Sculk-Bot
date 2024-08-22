import discord
from discord.ext import commands
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

from discord import app_commands

import modules.log as log

import json; data = json.load(open('config.json', 'r', encoding='utf-8'))

class UnlockCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.checks.has_any_role(*data['roles']['admin'])
    @app_commands.command(name='unlock', description='Unlocks the current room')
    async def unlock(self, interaction:discord.Interaction):
        await interaction.response.defer(thinking=False, ephemeral=True)

        await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)

        embed = discord.Embed(description='### The lounge has been successfully unlocked', colour=0x28b4d8)
        await interaction.followup.send(embed=embed)

        embed = discord.Embed(description='### The living room has been unlocked', colour=0x28b4d8)
        await interaction.channel.send(embed=embed)

    @unlock.error
    async def unlock_error(self, interaction:discord.Interaction, error):
        if isinstance(error, commands.MissingAnyRole):
            embed = discord.Embed(description='### Do not have permission to use this command', colour=0x28b4d8)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description='### An error has occurred', colour=0x28b4d8)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            log.write('cogs.commands.unlock', error, log.levels.error)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(UnlockCog(bot))