import discord
from discord.ext import commands

import json; data = json.load(open('config.json', 'r', encoding='utf-8'))
import modules.log as log
import asyncio

class autojoin(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        member.add_roles(member.guild.get_role(data['autorole']))
        log.write('cogs.events.autorole', f'{member} joined the server and was given the autorole role', log.levels.debug)
    
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        for guild in self.bot.guilds:
            for member in guild.members:
                if member.bot:
                    break
                if data['autorole'] not in [role.id for role in member.roles]:
                    await member.add_roles(member.guild.get_role(data['autorole']))
                    log.write('cogs.events.autorole', f'{member} received the autorole role because he did not possess it', log.levels.debug)
                    await asyncio.sleep(0.5)
    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(autojoin(bot))