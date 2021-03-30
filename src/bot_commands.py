from typing import List
import discord
from discord.ext import commands

from simple_discord_message import SimpleDiscordMessage

from default_config import DEFAULT_CONFIG

import card_game_handler as card_dealer
from card_game_logic.card_games.card_game_type import CardGameType

bot = commands.Bot(
    command_prefix=DEFAULT_CONFIG['prefix'], case_insensitive=True)
bot.card_games = {}


@bot.command()
async def test(ctx):
    await ctx.send(f"message info: \n{ctx.message}")

@bot.command()
async def bisca(ctx, members: commands.Greedy[discord.User]):
    author_id = ctx.message.author.id
    invalid_args_msg = validate_game_challenge_args(members=members, game_type=CardGameType.BISCA)
    if not invalid_args_msg is None:
        await send_simple_discord_message(channel=ctx, message=invalid_args_msg)
        return
        
    teams_dict = {author_id: 1, members[0].id: 2}
    if len(teams_dict) != 2:
        await ctx.send(f"{ctx.message.author.mention} repeated users in challenge....probably")
        return

    simple_message = card_dealer.create_card_game_challenge_handler(challenger=ctx.message.author, teams=teams_dict, members=members, game_type=CardGameType.BISCA)
    await send_simple_discord_message(channel=ctx, message=simple_message)

@bot.command()
async def show_last_challenges(ctx):
    challenges = card_dealer.get_last_n_challenges(10)
    message = "challenges:\n"
    for challen in challenges:
        message += f"{challen}\n"

    await ctx.send(message)

@bot.command()
async def show52deck(ctx):
    await send_simple_discord_message(ctx, card_dealer.show_52_deck_str())

@bot.command()
async def hitme(ctx):
    card = card_dealer.show_random_card()
    embed = discord.Embed(title=str(card), description="random card given")
    #embed.add_field(name="nice field", value="value")
    #embed.set_footer(text="your card", icon_url="https://cdn.discordapp.com/emojis/817060615079067718.png?v=1")
    embed.set_image(url=card_dealer.get_card_image_url(card))
    await ctx.send(content=ctx.message.author.mention, embed=embed)

@bot.event
async def on_raw_reaction_add(payload):
    user = bot.get_user(payload.user_id)

    if user == bot.user:
        return
    elif user is None:
        user = await bot.fetch_user(payload.user_id)

    ##defines channel
    if payload.guild_id is None:
        channel = user
        #channel = bot.get_channel(payload.channel_id)
    else:
        channel = bot.get_channel(payload.channel_id)

    message = await channel.fetch_message(payload.message_id)
    emoji = payload.emoji
    if message.author == bot.user:
        message.content.startswith("(card_games)")
        message_list = card_dealer.card_game_reaction_handler(emoji=emoji, message=message, user=user)

        if not message_list is None:
            for simple_message in message_list:
                if simple_message.channel is None:
                    channel = await bot.fetch_user(simple_message.channel_id)
                else:
                    channel = simple_message.channel
                await send_simple_discord_message(channel=channel, message=simple_message)

def validate_game_challenge_args(members: commands.Greedy[discord.User], game_type: CardGameType) -> SimpleDiscordMessage:
    extra_player = len(members) + 1 - game_type.value
    #None means theres no problems
    if game_type.value == 0 or extra_player == 0:
        return None
        
    elif extra_player > 0:
        return SimpleDiscordMessage(content=f"Number of users tagged exceeds the expected by {extra_player}")
    else:
        return SimpleDiscordMessage(content=f"Number of users tagged falls short by {extra_player}")

async def send_simple_discord_message(channel: discord.abc.Messageable, message: SimpleDiscordMessage):
    sent_message = await channel.send(content=message.content, embed=message.embed)

    for reaction in message.reactions:
        await sent_message.add_reaction(reaction)