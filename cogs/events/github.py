import discord
from discord.ext import commands

import requests
import re
import json

with open('config.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

class Github(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.github_url_pattern = re.compile(r'^https:\/\/github\.com\/sculkmp\/.*$')

    def get_github_file(self, url: str) -> tuple[str, str]:
        """Fetches a GitHub file and returns its content and format"""
        url = url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
        try:
            url, line = url.split('#L')
            line = int(line)
        except ValueError:
            return ('Invalid URL', None)

        response = requests.get(url)
        if response.status_code not in [200, 201]:
            return ('Invalid URL', None)

        lines = response.text.split('\n')
        start, end = max(0, line - 5), min(len(lines), line + 5)

        formatted_lines = []
        for i, line_content in enumerate(lines[start:end], start + 1):
            if i == line:
                formatted_lines.append(f'>{line_content}')
            else:
                formatted_lines.append(f'{i} {line_content}')

        return ('\n'.join(formatted_lines), url.split('.')[-1])

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return

        if not self.github_url_pattern.match(message.content):
            return

        content, format = self.get_github_file(message.content)

        if content == 'Invalid URL':
            embed = discord.Embed(description='### This is not a valid link', colour=0x28b4d8)
            return await message.reply(embed=embed)

        return await message.reply(f'```{format}\n{content}```')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Github(bot))