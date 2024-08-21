import discord
from discord.ext import commands
from discord import app_commands

import json; data = json.load(open('config.json', 'r', encoding='utf-8'))


class Info(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @app_commands.command(name='info', description='Get server information')
    async def info(self, interaction:discord.Interaction):
        members = len(interaction.guild.members)
        bots = len([member for member in interaction.guild.members if member.bot])
        humans = members - bots
        text_channels = len([channel for channel in interaction.guild.channels if isinstance(channel, discord.TextChannel)])
        voice_channels = len([channel for channel in interaction.guild.channels if isinstance(channel, discord.VoiceChannel)])
        categories = len([channel for channel in interaction.guild.channels if isinstance(channel, discord.CategoryChannel)])
        roles = len(interaction.guild.roles)
        emojis = len(interaction.guild.emojis)
        boosters = interaction.guild.premium_subscription_count
        boost_level = interaction.guild.premium_tier
        vanity_url = interaction.guild.vanity_url
        
        embed = discord.Embed(description=f'## Information on `{interaction.guild.name}`\n\u200b', colour=0x28b4d8)
        embed.add_field(name='Members', value=f'`👤` {humans}\n`🤖` {bots}', inline=True)
        embed.add_field(name='Channel', value=f'`📂` {categories}\n`💬` {text_channels}\n`🔊` {voice_channels}', inline=True)
        embed.add_field(name='Rank', value=f'`👾` {roles}', inline=True)
        
        embed.add_field(name='\u200b', value=f'\u200b', inline=True)
        
        embed.add_field(name='Emojis', value=f'`😄` {emojis}', inline=True)
        embed.add_field(name='Boosts', value=f'`👻` {boosters} boosts\n`🪙` level {boost_level}', inline=True)
        embed.add_field(name='Custom URL', value='`✨` ' + (vanity_url if vanity_url else 'none'), inline=True)
        
        await interaction.response.send_message(embed=embed)
        


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Info(bot))