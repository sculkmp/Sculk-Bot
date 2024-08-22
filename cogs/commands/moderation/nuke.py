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

import modules.log as log

import json; data = json.load(open('config.json', 'r', encoding='utf-8'))


class Nuke(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    
    @app_commands.checks.has_any_role(*data['roles']['admin'])
    
    @app_commands.command(name='nuke', description='Clear the current room and recreate it with the same settings')
    async def nuke(self, interaction:discord.Interaction):
        await interaction.response.defer(thinking=False)
        channel = await interaction.channel.clone()
        await interaction.channel.delete()
        embed = discord.Embed(description='### The salon was successfully cleared', colour=0x28b4d8)
        await channel.send(embed=embed)
        
    @nuke.error
    async def nuke_error(self, interaction:discord.Interaction, error):
        if isinstance(error, commands.MissingAnyRole):
            embed = discord.Embed(description='### Do not have permission to use this command', colour=0x28b4d8)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description='### An error has occurred', colour=0x28b4d8)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            log.write('cogs.commands.giveaway', error, log.levels.error)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Nuke(bot))