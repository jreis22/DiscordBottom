import numpy as np
from math import ceil
import discord
import uuid
from typing import List, Union

from simple_discord_message import SimpleDiscordMessage
from discord_card_game import DiscordCardGame
from discord_card_game_in_memory_repo import DiscordCardGameInMemoryRepo
from card_image_dictionary import CardImageDictionary

from card_game_logic.player import CardPlayer
#from card_game_logic.player_state import PlayerStateEnum

from card_game_logic.cards.card_enums import Rank, Suit
from card_game_logic.cards.card import PlayingCard

from card_game_logic.card_games.card_game import CardGame
from card_game_logic.card_games.played_card import PlayedCard
from card_game_logic.card_games.card_game_type import CardGameType
#from card_game_logic.card_games.card_game_factory import CardGameFactory
from card_game_logic.card_games.card_game_challenge import CardGameChallenge

from card_game_logic.repositories.in_memory_challenge_repository import InMemoryChallengeRepository
#from card_game_logic.repositories.in_memory_game_repository import InMemoryGameRepository

challenge_repo = InMemoryChallengeRepository()
game_repo = DiscordCardGameInMemoryRepo()

CARD_GAME_MESSAGE_STR = "♥️♣️♦️♠️"

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

#teams dict format: {user_id: team}
def create_card_game_challenge_handler(challenger: discord.User, teams: dict, members: List[discord.User], game_type: CardGameType) -> SimpleDiscordMessage:

    players = []
    try:
        validate_users_for_challenge(teams)
    except IOError as err:
        return SimpleDiscordMessage(str(err))

    for user_id in teams:
        player = create_new_player(user_id=user_id, team=teams[user_id]["TEAM"], player_name=teams[user_id]["NAME"])
        players.append(player)

    challenge = CardGameChallenge(
        challenger_id=challenger.id, players_list=players, game_type=game_type)
    challenge.accept_challenge(challenger.id)
    challenge_repo.insert(challenge)

######################################
    content = f"{CARD_GAME_MESSAGE_STR} challenge:"
    game_name = game_type.name.title()
    content += f", {challenger.mention} challenged you to a game of {game_name}"
    embed = discord.Embed(title=f"{game_name.name.title()} Challenge",
                          description=f"A challenge to a card game of {game_name}")
    embed.set_image(url=get_card_image_url(show_random_card()))
    embed.set_footer(text=str(challenge.id))
    # , icon_url="https://cdn.discordapp.com/emojis/817060615079067718.png?v=1")
    
    for member in members:
        content += f" {member.mention}"

    content += f", {challenger.mention} challenged you to a game of {game_name}"
    message = SimpleDiscordMessage(
        content=content, embed=embed, reactions=["✅", "❌"])

    return message


def validate_users_for_challenge(users: dict):
    users_len = len(users)
    ids = list(users.keys())
    for i in range(users_len - 1):
        if ids[i] in ids[i + 1:]:
            raise IOError(f"User <@{ids[i]}> repeated")


def create_new_player(user_id, player_name: str, team=0):
    return CardPlayer(player_id=user_id, team=team, player_name=player_name)


def create_game_from_challenge(challenge) -> CardGame:
    return challenge.create_card_game()


def get_last_n_challenges(n: int) -> list:
    return challenge_repo.get_last_n_entries(n)

# handles card games related messages


def card_game_reaction_handler(emoji: discord.PartialEmoji, message: discord.Message, user: discord.User) -> List[SimpleDiscordMessage]:
    #    if isinstance(channel, discord.User):
    #        await channel.send("nice dm react")
    #    else:
    #        await channel.send("nice card_games reaction")
    # if isinstance(channel, discord.user):
    #   if()

    if "challenge:" in message.content:
        return card_game_challenge_reaction_handler(emoji=emoji, message=message, user=user)
    elif "card_selection:" in message.content:
        return card_game_card_selection_handler(emoji=emoji, message=message, user=user)

######## handles card games challenges


def card_game_challenge_reaction_handler(emoji: discord.PartialEmoji, message: discord.Message, user: discord.User) -> List[SimpleDiscordMessage]:
    challenge_id = get_challlenge_id_from_message(message=message)
    if not challenge_repo.has(challenge_id=challenge_id):
        content = f"{user.mention}, challenge can't be found in the database"
        return [SimpleDiscordMessage(content=content, channel=message.channel)]

    #challenge validation
    challenge = challenge_repo.get_by_id(challenge_id)
    content = None
    message_list = []
    
    if not challenge.has_player(user.id):
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
            discord_game = create_card_game_handler(challenge=challenge, messageable=message.channel)
            message_list += get_all_players_card_dm(game=discord_game.get_game())

            content += "\nChallenge was accepted, game was created"
            try:
                trump_suit = discord_game.game.trump_suit
                if trump_suit != Suit.JOKER:
                    content += f"\ntrump suit: {CardImageDictionary.get_suit_emoji(suit=trump_suit)} ({trump_suit.name.title()})"
            except AttributeError:
                pass
            try:
                last_card = discord_game.game.last_card
                content += f"\nlast card: {CardImageDictionary.get_card_emoji(suit=last_card.suit, rank=last_card.rank)} ({last_card})"
                if discord_game.game.last_card_owner:
                    content += f"  belongs to {discord_game.game.get_player_name(discord_game.game.last_card_owner)}"
            except AttributeError:
                pass        

            message_list.append(get_next_player_message(discord_game=discord_game))

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

##### handles card game reactions
def card_game_card_selection_handler(emoji: discord.PartialEmoji, message: discord.Message, user: discord.User) -> List[SimpleDiscordMessage]:
    #emoji validation (done in the beginning to save time on wrong emoji reacts)
    if emoji.id is None:
        return None
    elif not CardImageDictionary.is_card_emoji(emoji):
        return None

    #check if game is in the database (all validations are done from the game, so it has to be validated right away)
    game_id = get_game_id_from_message(message=message)

    if not game_repo.has(game_id=game_id):
        content = "Game can't be found in the database"
        return [SimpleDiscordMessage(content=content, channel=user)]

    discord_game = game_repo.get_by_id(game_id)
    #game validation
    game = discord_game.get_game()
    content = None
    message_list = []
    channel = user
    if not game.has_player(user.id):
        content = f"{user.mention} you are not a part of that game"

    elif game.is_game_over():
        content = "Game has already ended"
        simple_message = SimpleDiscordMessage(
            content=content, channel=channel)
        message_list.append(simple_message)

    # elif game.is_game_over():
    #     content = "Game has already ended"
    #     simple_message = SimpleDiscordMessage(
    #         content=content, channel=channel)
    #     message_list.append(simple_message)
    else:
        #try:
        card = CardImageDictionary.get_card_by_id(emoji.id)
        discord_game.game.play_card(player_key=user.id, card=card)
        game_repo.update(game_id=discord_game.get_id(), game=discord_game)
        message_list.append(get_card_played_server_message(user=user, card=card, discord_game=discord_game))
        #except Exception as e:
            #message_list.append(SimpleDiscordMessage(content=str(e), channel=user))

        if not game.is_game_over():
            if game.is_round_start():
                message_list += get_all_players_card_dm(game=game)
            message_list.append(get_next_player_message(discord_game=discord_game))
        else:
            winners_str= "Game Winner"
            winners = game.get_game_winners()
            if len(winners) > 1:
                winners_str += "s"
            winners_str += ":"
            for winner in winners:
                winners_str += f" <@{winner}>"
            message_list.append(SimpleDiscordMessage(content=winners_str, channel=discord_game.channel))

    return message_list

def get_card_played_server_message(user: discord.User, card:PlayingCard, discord_game: DiscordCardGame) -> SimpleDiscordMessage:
    embed = get_table_embed(game=discord_game.game)
    message = SimpleDiscordMessage(content=f"{user.mention} has played {card} {CardImageDictionary.get_card_emoji(suit=card.suit, rank=card.rank)}", embed=embed, channel=discord_game.channel)
    return message

def get_next_player_message(discord_game: DiscordCardGame) -> SimpleDiscordMessage:
    if discord_game.game.is_game_over():
        return get_game_over_message(discord_game=discord_game)

    next_player = discord_game.game.get_next_player()
    message = card_select_dm(player_id=next_player.player_id, game=discord_game.game,
                                cards=get_player_valid_cards(player_id=next_player.player_id, card_game=discord_game.game))
    return message

def get_game_over_message(discord_game: DiscordCardGame):
    content = "Game has ended"

    winning_team = discord_game.game.get_winning_players()

    embed = discord.Embed(title=f"Game Over")
    embed.add_field(name="Winners:", value=get_winners_string(winning_team))
    embed.set_footer(text=str(discord_game.game.get_id()))

    message = SimpleDiscordMessage(content=content, embed=embed, reactions=["🔄", "↪️"], channel=discord_game.channel)

    return message

def get_winners_string(winners_ids: list) -> str:
    string =""
    for id in winners_ids:
        string += f"<@{id}> "

def get_game_id_from_message(message: discord.Message):
    embed = message.embeds[0]
    return uuid.UUID(embed.to_dict()['footer']['text'])

def get_game_round_from_message(message: discord.Message) -> int:
    embed = message.embeds[0]
    return int(embed.description.split()[1])

# creates card game and saves it in repo
def create_card_game_handler(challenge: CardGameChallenge, messageable: discord.abc.Messageable) -> DiscordCardGame:
    card_game = create_game_from_challenge(challenge)
    discord_game = DiscordCardGame(game=card_game, channel=messageable)
    game_repo.insert(discord_game)
    return discord_game


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


def player_cards_dm(user, cards: List[PlayingCard]) -> SimpleDiscordMessage:
    content = f"{CARD_GAME_MESSAGE_STR} card_hand:"
    embed = discord.Embed(title="Your cards", description=cards_to_emoji(cards))
    message = SimpleDiscordMessage(content=content, embed=embed, channel=user)
    return message

def get_all_players_card_dm(game: CardGame) -> List[SimpleDiscordMessage]:
    message_list = []
    for player_id in game.players:
        #print(f"player: {player_id}")
        cards = game.players[player_id].show_hand()
        message_list.append(player_cards_dm(user=player_id, cards=cards))
    return message_list

def card_select_dm(cards: List[PlayingCard], player_id, game: CardGame):
    content = f"{CARD_GAME_MESSAGE_STR} card_selection:"
    embed = discord.Embed(title="Pick a card", description=f"Round: {game.current_round}")
    if game.trump_suit and game.trump_suit != Suit.JOKER:
        suit = game.trump_suit
        value = f"{CardImageDictionary.get_suit_emoji(suit=suit)} ({suit.name.title()})"
        embed.add_field(name="Trump Suit", value=value)
    embed.set_footer(text=str(game.get_id()))
    return SimpleDiscordMessage(content=content, embed=embed, reactions=cards_to_emoji_list(cards), channel=player_id)


def get_player_valid_cards(player_id, card_game: Union[uuid.UUID, CardGame]) -> List[PlayingCard]:
    if isinstance(card_game, CardGame):
        game = card_game
    else:
        game = game_repo.get_by_id(card_game)

    return game.get_player_valid_cards(player_key=player_id)

####### UNFINISHED CAUSE IT SUCKS (also you cant tag users in embeds)
def get_table_embed(game: CardGame) -> discord.Embed:
    #used so that the first player in the table is always the same
    top_player_id = game.first_player_id

    #get the players by order and the plays made
    player_order = game.get_player_order()
    n_players = len(game.players)
    plays = game.get_plays_from_last_played_round()
    n_plays = len(plays)
    #if the player was the last playing, then the round is over so it needs to show the previous round(where the last player played)
    is_end_round = game.is_round_start() #if its the start of the round, we show the end of previous round
    n_players_is_odd = True if (n_players % 2) != 0 else False
    #get first player index
    top_player_index = 0
    first_player_id = plays[0].player_key if n_plays > 0 else player_order[0]
    i=0
    offset = 0
    #print(f"N_PLAYS: {n_plays}")
    for player_id in player_order:
        if player_id == top_player_id:
            top_player_index = i
              
        #checks if player order is the same as the order that the round was played
        if player_id == first_player_id:
            offset = i
        i += 1

    #done so the player order and plays order have the same order
    if offset != 0:
        player_order = player_order[offset:] + player_order[:offset]
    
    #update the top player index post rotation
    top_player_index += offset
    if top_player_index >= n_players:
        top_player_index -= n_players

    game_round = plays[0].round if n_plays > 0 else game.current_round
    embed = discord.Embed(title="Player table", description=f"Round: {game_round}")
    players_added = 0
    #number used to know if there is plays still to be added
    while players_added < n_players:
        player_index = top_player_index + (players_added >> 1) + (1 * n_players_is_odd * players_added > 0)
        if player_index >= n_players:
            player_index -= n_players

        #gets the info of at least 1 player
        player_name = game.get_player_name(player_order[player_index])
        card = plays[player_index] if player_index < n_plays else None
        if (n_players_is_odd and players_added == 0) or players_added == n_players - 1:
            add_single_player_line_to_embed(player_name = player_name, embed=embed, played_card=card)
        else:
            player2_index = top_player_index - 1 - (players_added >> 1)

            if player2_index < 0:
                player2_index += n_players

            player2name = game.get_player_name(player_order[player2_index])
            card2 = plays[player2_index] if player2_index < n_plays else None

            #print(f"card1: {card}     card2: {card2} \n plays: {n_plays}\n player1_index: {player_index}   player2_index: {player2_index}")
            players_added += 1
            #adds a shorter line if its the last line or if its the first line in a even player game
            if (n_players - players_added) == 2 or players_added == 0: 
                add_two_player_close_line_to_embed(player1name = player_name, player2name = player2name 
                , embed=embed , played_card1=card , played_card2=card2)
            else:
                add_two_player_line_to_embed(player1name = player_name, player2name = player2name 
                , embed=embed , played_card1=card , played_card2=card2)
            

        players_added += 1
        if is_end_round:
            embed.add_field(name="Round Winner", value= game.get_player_name(game.get_round_winner(current_round=game_round)), inline=False)

    return embed

def add_single_player_line_to_embed(player_name, embed: discord.Embed, played_card: PlayedCard):
    cardstr = CardImageDictionary.get_card_emoji(rank=played_card.card.rank, suit=played_card.card.suit) if not played_card is None else " "
    embed.add_field(name=f"{player_name}", value=cardstr)
    return

def add_two_player_line_to_embed(player1name, player2name, embed: discord.Embed, played_card1: PlayedCard, played_card2: PlayedCard):
    card1str = CardImageDictionary.get_card_emoji(rank=played_card1.card.rank, suit=played_card1.card.suit) if not played_card1 is None else "\u00A0"
    card2str = CardImageDictionary.get_card_emoji(rank=played_card2.card.rank, suit=played_card2.card.suit) if not played_card2 is None else "\u00A0"
    name = f"{player1name}" + f"\u00A0" * 16 + player2name  #adds spaces with a different char so discord wont delete them
    line_value = f"{card1str}" + f"\u00A0" * (16 + (len(player1name)-1)) + card2str
    embed.add_field(name=name, value=line_value)
    #embed.add_field(name=f"        ", value="        ")
    #embed.add_field(name=f"    {player2name}", value=f"    {card2str}", inline=True)

def add_two_player_close_line_to_embed(player1name, player2name, embed: discord.Embed, played_card1: PlayedCard, played_card2: PlayedCard):
    card1str = CardImageDictionary.get_card_emoji(rank=played_card1.card.rank, suit=played_card1.card.suit) if not played_card1 is None else "\u00A0"
    card2str = CardImageDictionary.get_card_emoji(rank=played_card2.card.rank, suit=played_card2.card.suit) if not played_card2 is None else "\u00A0"
    name = f"{player1name}" + "\u00A0" * 8 + player2name
    line_value = f"{card1str}" + "\u00A0" * (8 + (len(player1name)-1)) + card2str
    embed.add_field(name=name, value=line_value)
    #embed.add_field(name="     ", value="     ")
    #embed.add_field(name=f"   {player2name}", value=f"   {card2str}", inline=True)

#useless
def get_table_message_string(game: CardGame) -> str:
    n_players = len(game.players)
    plays = game.get_plays_from_current_round()
    n_plays = len(plays)

    plays_added = 0
    message = ""

    while plays_added < n_players:
        if plays_added == 0:
            if n_players == 4 or n_players % 2 != 0:
                message += f""
