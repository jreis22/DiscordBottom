import numpy as np
import discord
import uuid
from typing import List, Union

from simple_discord_message import SimpleDiscordMessage

from card_image_dictionary import CardImageDictionary

from card_game_logic.player import CardPlayer
#from card_game_logic.player_state import PlayerStateEnum

from card_game_logic.cards.card_enums import Rank, Suit
from card_game_logic.cards.card import PlayingCard

from card_game_logic.card_games.card_game import CardGame
from card_game_logic.card_games.card_game_type import CardGameType
#from card_game_logic.card_games.card_game_factory import CardGameFactory
from card_game_logic.card_games.card_game_challenge import CardGameChallenge

from card_game_logic.repositories.in_memory_challenge_repository import InMemoryChallengeRepository
from card_game_logic.repositories.in_memory_game_repository import InMemoryGameRepository

challenge_repo = InMemoryChallengeRepository()
game_repo = InMemoryGameRepository()


def show_random_card() -> PlayingCard:
    rank = np.random.choice(Rank.get_all())
    suit = np.random.choice(Suit.get_all())

    return PlayingCard(rank=rank, suit=suit)


def show_52_deck_str() -> SimpleDiscordMessage:
    string = ""
    for suit in Suit.get_all():
        for rank in Rank.get_all():
            string = string + \
                CardImageDictionary.get_card_emoji(rank=rank, suit=suit)
    message = SimpleDiscordMessage(content=string)
    return message


def get_card_image_url(card: PlayingCard) -> str:
    return CardImageDictionary.get_card_image_url(rank=card.rank, suit=card.suit)


def get_card_emoji(card: PlayingCard) -> str:
    return CardImageDictionary.get_card_emoji(rank=card.rank, suit=card.suit)

# users is a dictionary in which key is the user.id and the value is their team


def create_card_game_challenge_handler(challenger: discord.User, teams: {}, members: List[discord.User], game_type: CardGameType) -> SimpleDiscordMessage:

    players = []
    try:
        validate_users_for_challenge(teams)
    except IOError as err:
        return SimpleDiscordMessage(str(err))

    for user_id in teams:
        player = create_new_player(user_id=user_id, team=teams[user_id])
        players.append(player)

    challenge = CardGameChallenge(
        challenger_id=challenger.id, players_list=players, game_type=game_type)
    challenge.accept_challenge(challenger.id)
    challenge_repo.insert(challenge)

######################################
    embed = discord.Embed(title=f"{game_type.name} Challenge",
                          description=f"A challenge to a card game of {game_type.name}")
    embed.set_image(url=get_card_image_url(show_random_card()))
    embed.set_footer(text=str(challenge.id))
    # , icon_url="https://cdn.discordapp.com/emojis/817060615079067718.png?v=1")
    content = f"(card_games) <challenge>:"
    for member in members:
        content += f" {member.mention}"

    content += f", {challenger.mention} challenged you to a game of {game_type.name}"
    message = SimpleDiscordMessage(
        content=content, embed=embed, reactions=["✅", "❌"])

    return message


def validate_users_for_challenge(users: {}):
    users_len = len(users)
    ids = list(users.keys())
    for i in range(users_len - 1):
        if ids[i] in ids[i + 1:]:
            raise IOError(f"User <@{ids[i]}> repeated")


def create_new_player(user_id, team=0):
    return CardPlayer(player_id=user_id, team=team)


def create_game_from_challenge(challenge):
    return challenge.create_card_game()


def get_last_n_challenges(n: int) -> []:
    return challenge_repo.get_last_n_entries(n)

# handles card games related messages


def card_game_reaction_handler(emoji: discord.emoji, message: discord.Message, user: discord.User) -> List[SimpleDiscordMessage]:
    #    if isinstance(channel, discord.User):
    #        await channel.send("nice dm react")
    #    else:
    #        await channel.send("nice card_games reaction")
    # if isinstance(channel, discord.user):
    #   if()

    if "<challenge>" in message.content:
        return card_game_challenge_reaction_handler(emoji=emoji, message=message, user=user)

# handles card games challenges


def card_game_challenge_reaction_handler(emoji: discord.emoji, message: discord.Message, user: discord.User) -> List[SimpleDiscordMessage]:
    challenge_id = get_challlenge_id_from_message(message=message)
    challenge = challenge_repo.get_by_id(challenge_id)
    content = None
    message_list = []
    if challenge is None:
        content = "Challenge can't be found in the database"

    elif not challenge.has_player(user.id):
        content = f"{user.mention} you are not a part of that challenge/game"

    elif challenge.is_accepted():
        content = "Challenge was already accepted, can't change answer now"

    elif challenge.is_cancelled():
        content = "Challenge was already denied, can't change answer now"

    elif str(emoji) == "✅":
        challenge.accept_challenge(user.id)
        challenge_repo.update(challenge_id=challenge.id, challenge=challenge)
        content = f"{user.mention} Accepted the challenge"

        if challenge.is_accepted():
            game = create_card_game_handler(challenge=challenge)

            for player_id in game.players:
                cards = game.players[player_id].show_hand()
                message_list.append(SimpleDiscordMessage(
                    content=player_cards_dm(cards=cards), channel=player_id))

            content += f"\nChallenge was accepted, game was created"
            first_player = game.get_first_player()
            message_list.append(card_select_dm(player_id=first_player.player_id, game=game,
                                               cards=get_player_valid_cards(player_id=first_player.player_id, card_game=game)))

    elif str(emoji) == "❌":
        challenge.quit_challenge(user.id)
        challenge_repo.update(challenge_id=challenge.id, challenge=challenge)
        content = f"{user.mention} dropped out of the chalenge, game was cancelled"

    channel = message.channel
    if content is None:
        return None

    simple_server_message = SimpleDiscordMessage(
        content=content, channel=channel)
    message_list.append(simple_server_message)
    return message_list

# filters message content/embed to obtain challenge id


def get_challlenge_id_from_message(message: discord.Message):
    embed = message.embeds[0]
    return uuid.UUID(embed.to_dict()['footer']['text'])

# creates card game and saves it in repo


def create_card_game_handler(challenge: CardGameChallenge) -> CardGame:
    card_game = create_game_from_challenge(challenge)
    game_repo.insert(card_game)
    return card_game


def cards_to_emoji(cards: List[PlayingCard]) -> str:
    string = ""
    for card in cards:
        string += CardImageDictionary.get_card_emoji(
            rank=card.rank, suit=card.suit)

    return string


def cards_to_emoji_list(cards: List[PlayingCard]) -> List[str]:
    cardl = []
    for card in cards:
        cardl.append(CardImageDictionary.get_card_emoji(
            rank=card.rank, suit=card.suit))
    return cardl


def player_cards_dm(cards) -> str:
    return f"(card_games) <card_hand>:\n{cards_to_emoji(cards)}"


def card_select_dm(cards: PlayingCard, player_id, game: CardGame):
    content = "(card_games) <card_selection> Select the card you wish to play"
    embed = discord.Embed(title="Pick a card")
    embed.set_footer(text=str(game.get_id()))
    return SimpleDiscordMessage(content=content, embed=embed, reactions=cards_to_emoji_list(cards), channel=player_id)


def get_player_valid_cards(player_id, card_game: Union[uuid.UUID, CardGame]) -> List[PlayingCard]:
    if isinstance(card_game, CardGame):
        game = card_game
    else:
        game = game_repo.get_by_id(card_game)

    return game.get_player_valid_cards(player_key=player_id)
