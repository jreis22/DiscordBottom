import discord
from discord.ext import commands
import json

bot = commands.Bot(command_prefix='!')


@bot.command()
async def ping(ctx):
    await ctx.send('pong')

with open('user-config.json', 'r') as f:
    config = json.load(f)

bot.run(config['TOKEN'])
