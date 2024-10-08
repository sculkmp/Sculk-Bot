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


class form(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Message")

    answer = discord.ui.TextInput(label="Content", placeholder="Hey, how are you", style=discord.TextStyle.long, max_length=4000, required=True)
    color = discord.ui.TextInput(label="Color", placeholder="2d2d31", style=discord.TextStyle.short, min_length=6, max_length=6, required=True)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        try:
            await interaction.response.defer(thinking=False, ephemeral=False)
            embed = discord.Embed(description=self.answer.value, color=int(self.color.value, 16))
            embed.set_author(name=interaction.guild.name, icon_url=interaction.guild.icon.url)
            await interaction.channel.send(embed=embed)
        except ValueError:
            embed = discord.Embed(description='### The colour must be hexadecimal', colour=0x28b4d8)
            await interaction.channel.send(embed=embed)


class sayCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @app_commands.checks.has_any_role(*data['roles']['admin'])

    @app_commands.command(name='say', description='Send a custom embed message')
    async def say(self, interaction:discord.Interaction):
        await interaction.response.send_modal(form())

    @say.error
    async def say_error(self, interaction:discord.Interaction, error):
        if isinstance(error, commands.MissingAnyRole):
            embed = discord.Embed(description='### you do not have permission to use this command', colour=0x28b4d8)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description='### An error occurred', colour=0x28b4d8)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            log.write('cogs.commands.say', error, log.levels.error)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(sayCog(bot))