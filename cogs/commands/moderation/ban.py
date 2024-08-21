import discord
from discord.ext import commands
from discord import app_commands
import datetime

import modules.log as log

import json; data = json.load(open('config.json', 'r', encoding='utf-8'))

class BanCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.checks.has_any_role(*data['roles']['admin'])
    @app_commands.command(name='ban', description='Bans a member from the server')
    async def ban(self, interaction:discord.Interaction, member: discord.Member, time: str = None, reason: str = None):
        await interaction.response.defer(thinking=False, ephemeral=True)

        if member == interaction.user:
            embed = discord.Embed(description='### You cannot ban yourself', colour=0x28b4d8)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if member.guild_permissions.administrator:
            embed = discord.Embed(description='### You cannot ban an administrator', colour=0x28b4d8)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if time:
            try:
                time = datetime.datetime.strptime(time, '%d-%m-%Y %H:%M:%S')
            except ValueError:
                embed = discord.Embed(description='### Invalid time format. Please use DD-MM-YYYY HH:MM:SS', colour=0x28b4d8)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            await member.ban(reason=reason)
            await self.bot.schedule_task(time, self.unban, member)

            embed = discord.Embed(description=f'### {member.mention} has been banned until {time.strftime("%d-%m-%Y %H:%M:%S")}', colour=0x28b4d8)
            await interaction.followup.send(embed=embed)

            embed = discord.Embed(description=f'### {member.mention} has been banned for {reason} until {time.strftime("%d-%m-%Y %H:%M:%S")}', colour=0x28b4d8)
            await interaction.channel.send(embed=embed)
        else:
            await member.ban(reason=reason)

            embed = discord.Embed(description=f'### {member.mention} has been banned', colour=0x28b4d8)
            await interaction.followup.send(embed=embed)

            embed = discord.Embed(description=f'### {member.mention} has been banned for {reason}', colour=0x28b4d8)
            await interaction.channel.send(embed=embed)

    @ban.error
    async def ban_error(self, interaction:discord.Interaction, error):
        if isinstance(error, commands.MissingAnyRole):
            embed = discord.Embed(description='### Do not have permission to use this command', colour=0x28b4d8)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(description='### Please specify a member to ban', colour=0x28b4d8)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(description='### An error has occurred', colour=0x28b4d8)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            log.write('cogs.commands.ban', error, log.levels.error)

    async def unban(self, member):
        await member.guild.unban(member)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BanCog(bot))