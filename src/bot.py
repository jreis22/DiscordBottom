import discord
from discord.ext import commands
from default_config import DEFAULT_CONFIG


class Bot(discord.Client):
    def __init__(self, config=DEFAULT_CONFIG):
        super().__init__()
        self.config = config
        self.client = commands.Bot(command_prefix=config['prefix'])

    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send(f'pong{round(self.latency * 1000)}ms')

    def log_in(self):
        self.run(self.config["TOKEN"])
