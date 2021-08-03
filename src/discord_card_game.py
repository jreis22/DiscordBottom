from discord.abc import Messageable
from card_game_logic.card_games.card_game import CardGame
class DiscordCardGame:
    PLAYER_NAME_MAX_LENGTH = 7
    #player names_dict format {player_id: player_name}
    def __init__(self, game: CardGame, channel: Messageable):
        self.set_game(game=game)
        self.set_channel(channel=channel)

    def get_id(self):
        return self.id

    def set_game(self, game: CardGame):
        self.game = game

    def get_game(self) -> CardGame:
        return self.game

    def set_channel(self, channel: Messageable):
        self.channel = channel

    def get_channel(self) -> Messageable:
        return self.channel