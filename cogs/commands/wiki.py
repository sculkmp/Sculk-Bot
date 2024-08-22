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

class Wiki(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='wiki', description='Get wiki information')
    async def wiki(self, interaction: discord.Interaction):
        wiki_url = 'https://www.sculkmp.org/wiki'
        embed = discord.Embed(description=f'You can find more information on our wiki: [Click here]({wiki_url})', colour=0x28b4d8)
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Wiki(bot))