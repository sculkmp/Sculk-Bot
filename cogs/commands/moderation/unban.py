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
from discord import app_commands
from discord.ext import commands

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="unban", description="Unban a member")
    @app_commands.checks.has_role("Admin")
    async def unban(self, interaction: discord.Interaction, user_id: int):
        """Unban member via slash command"""
        guild = interaction.guild
        try:
            ban_entry = await guild.fetch_ban(discord.Object(id=user_id))
            await guild.unban(ban_entry.user)
            await interaction.response.send_message(f"User {ban_entry.user.mention} has been successfully unbanned!")
        except discord.NotFound:
            await interaction.response.send_message("This user is not banned.")
        except discord.Forbidden:
            await interaction.response.send_message("You don't have permission to unban this member.")
        except discord.HTTPException:
            await interaction.response.send_message("An error has occurred while trying to unban the user.")

    @unban.error
    async def unban_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("You don't have the required role to use this command.", ephemeral=True)
        else:
            await interaction.response.send_message("An unexpected error occurred.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Unban(bot))
