import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta

import modules.log as log

import json; data = json.load(open('config.json', 'r', encoding='utf-8'))

class MuteCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.checks.has_any_role(*data['roles']['admin'])
    @app_commands.command(name='mute', description='Mute a member for a specified duration')
    async def mute(self, interaction: discord.Interaction, member: discord.Member, duration: str):
        await interaction.response.defer(ephemeral=False)
        try:
            duration_seconds = self.parse_duration(duration)
            until = discord.utils.utcnow() + timedelta(seconds=duration_seconds)
            await member.timeout(until, reason='Muted by an administrator')
            embed = discord.Embed(description=f'### {member.mention} has been muted for {duration}', colour=0x28b4d8)
            await interaction.channel.send(embed=embed)
        except ValueError:
            embed = discord.Embed(description='### Invalid duration format. Use `Xd Yh Zm` or `Xs`', colour=0x28b4d8)
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(description='### An error occurred', colour=0x28b4d8)
            await interaction.followup.send(embed=embed, ephemeral=True)
            log.write('cogs.commands.mute', e, log.levels.error)

    def parse_duration(self, duration: str) -> int:
        duration = duration.replace(' ', '')
        seconds = 0
        if 'd' in duration:
            days = int(duration.split('d')[0])
            seconds += days * 86400
            duration = duration.split('d')[1]
        if 'h' in duration:
            hours = int(duration.split('h')[0])
            seconds += hours * 3600
            duration = duration.split('h')[1]
        if 'm' in duration:
            minutes = int(duration.split('m')[0])
            seconds += minutes * 60
            duration = duration.split('m')[1]
        if 's' in duration:
            seconds += int(duration.split('s')[0])
        return seconds

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MuteCog(bot))