import discord
from discord.ext import commands
import json

class Blacklist(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.blacklist = self.load_blacklist()

    def load_blacklist(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            return config['blacklist']

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        for mot in self.blacklist:
            if mot in message.content.lower():
                await message.delete()
                embed = discord.Embed(description=f'Le mot "{mot}" is blacklisted on this server.', colour=0x28b4d8)
                await message.channel.send(embed=embed, delete_after=5)
                return

    @commands.command(name='blacklist-add', description='Add a word to the blacklist')
    async def blacklist_add(self, ctx: commands.Context, mot: str):
        self.blacklist.append(mot.lower())
        self.save_blacklist()
        embed = discord.Embed(description=f'Le mot "{mot}" has been added to the blacklist.', colour=0x28b4d8)
        await ctx.send(embed=embed)

    @commands.command(name='blacklist-remove', description='Remove a word from the blacklist')
    async def blacklist_remove(self, ctx: commands.Context, mot: str):
        if mot.lower() in self.blacklist:
            self.blacklist.remove(mot.lower())
            self.save_blacklist()
            embed = discord.Embed(description=f'Le mot "{mot}" has been removed from the blacklist.', colour=0x28b4d8)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description=f'Le mot "{mot}" is not in the blacklist.', colour=0x28b4d8)
            await ctx.send(embed=embed)

    def save_blacklist(self):
        with open('config.json', 'w') as f:
            json.dump({'blacklist': self.blacklist}, f)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Blacklist(bot))