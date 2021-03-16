import discord
from discord.ext import commands
from default_config import DEFAULT_CONFIG
import card_game_handler as card_dealer

bot = commands.Bot(
    command_prefix=DEFAULT_CONFIG['prefix'], case_insensitive=True)
bot.card_games = {}


@bot.command()
async def test(ctx, arg):
    await ctx.send(ctx.message)


@bot.command()
async def challenge(ctx, user: discord.User):
    await ctx.send(user)


@bot.command()
async def bisca(ctx, user: discord.User):
    message = await (ctx.send(f"(card_game challenge): <@{user.id}>, <@{ctx.message.author.id}> challenged you to a game of bisca"))
    await message.add_reaction("✅")
    await message.add_reaction("❌")

@bot.command()
async def show_52_deck(ctx):
    await ctx.send("not yet")

@bot.command()
async def hit_me(ctx):
    card = card_dealer.show_random_card()
    await ctx.send(f"{card}  <@{ctx.message.author.id}>")

@bot.event
async def on_raw_reaction_add(payload):
    user = bot.get_user(payload.user_id)
    
    if user == bot.user:
        return
    elif user is None:
        #print("fetch user second try")
        user = await bot.fetch_user(payload.user_id)
    #print("user: ")
    #print(user)
    #print(payload)
    if payload.guild_id is None:
        channel = user
        #channel = bot.get_channel(payload.channel_id)
    else:
        channel = bot.get_channel(payload.channel_id)

    message = await channel.fetch_message(payload.message_id)
    if message.author == bot.user:
        await channel.send(f"nice reaction <@{user.id}>")
        await card_game_reaction_handler(message, user, channel)
        


async def card_game_reaction_handler(message: discord.Message, user: discord.User, channel):
    if isinstance(channel, discord.User):
        await channel.send("nice dm react")

    await message.add_reaction("<:SPADES_10:817418774378315776>")
