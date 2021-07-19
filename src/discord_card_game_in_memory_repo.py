import copy
from discord_card_game import DiscordCardGame

class DiscordCardGameInMemoryRepo:
    def __init__(self):
        self.games = {}

    def get_by_id(self, game_id) -> DiscordCardGame:
        return copy.copy(self.games[game_id])

    def insert(self, game: DiscordCardGame) -> bool:
        self.games[game.get_id()] = game
        return True

    def update(self, game_id, game: DiscordCardGame) -> bool:
        self.games[game_id] = game
        return True

    def has(self, game_id) -> bool:
        return game_id in self.games
