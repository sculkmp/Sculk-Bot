import discord
from discord.ext import commands
from discord import app_commands
import datetime

import modules.log as log

import json; data = json.load(open('config.json', 'r', encoding='utf-8'))

class KickCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.checks.has_any_role(*data['roles']['admin'])
    @app_commands.command(name='kick', description='Kicks a member from the server')
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        await interaction.response.defer(thinking=False, ephemeral=True)

        if member == interaction.user:
            embed = discord.Embed(description='### You cannot kick yourself', colour=0x28b4d8)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if member.guild_permissions.administrator:
            embed = discord.Embed(description='### You cannot kick an administrator', colour=0x28b4d8)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        await member.kick(reason=reason)

        embed = discord.Embed(description=f'### {member.mention} has been kicked', colour=0x28b4d8)
        await interaction.followup.send(embed=embed)

        embed = discord.Embed(description=f'### {member.mention} has been kicked for {reason}', colour=0x28b4d8)
        await interaction.channel.send(embed=embed)

    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, commands.MissingAnyRole):
            embed = discord.Embed(description='### Do not have permission to use this command', colour=0x28b4d8)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description='### Please specify a member to kick', colour=0x28b4d8)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description='### An error has occurred', colour=0x28b4d8)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            log.write('cogs.commands.kick', error, log.levels.error)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(KickCog(bot))