import discord
from discord.ext import commands

import requests
import re
import json; data = json.load(open('config.json', 'r', encoding='utf-8'))



class Github(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    def get_github_file(self, url:str) -> tuple[str, str]:
        url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')

        splitted_url = url.split('#L')
        if len(splitted_url) != 2:
            return ('Invalid URL', None)

        url = splitted_url[0]
        line = splitted_url[1]

        response = requests.get(url)
        if response.status_code not in [200, 201]:
            return ('Invalid URL', None)

        lines = response.text.split('\n')
        start = max(0, int(line) - 5)
        end = min(len(lines), int(line) + 5)

        for i in range(start, end):
            lines[i] = f' {i + 1} {lines[i]}'

        lines[int(line) - 1] = f'>{lines[int(line) - 1][1:]}'

        return ('\n'.join(lines[start:end]), url.split('.')[-1])

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        pattern = re.compile(r'^https:\/\/github\.com\/sculkmp\/.*$')
        if not pattern.match(message.content):
            return

        content, format = self.get_github_file(message.content)

        if content == 'Invalid URL':
            embed = discord.Embed(description='### This is not a valid link', colour=0x28b4d8)
            return await message.reply(embed=embed)

        return await message.reply(f'```{format}\n{content}```')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Github(bot))