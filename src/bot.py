import discord
from discord.ext import commands
from default_config import DEFAULT_CONFIG


class Bot:
    def __init__(self, config=DEFAULT_CONFIG):
        self.config = config
        self.client = commands.Bot(command_prefix=config['prefix'])

    def log_in(self):
        return self.client.run(self.config['TOKEN'])
