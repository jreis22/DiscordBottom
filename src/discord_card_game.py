from discord.abc import Messageable
from card_game_logic.card_games.card_game import CardGame
class DiscordCardGame:
    PLAYER_NAME_MAX_LENGTH = 7
    #player names_dict format {player_id: player_name}
    def __init__(self, game: CardGame, channel: Messageable, player_names_dict: dict = None):
        self.set_game(game=game)
        self.set_channel(channel=channel)
        self.id = game.get_id()
        self.set_player_names(player_names_dict) 

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

    def get_player_name(self, player_id)-> str:
        return self.player_names_dict[player_id]

    #if the player_names dictionary contains ids not present in the game, they will be ignored
    def set_player_names(self, player_names: dict):
        #if dict is empty names will be the ids
        if player_names is None:
            ids = self.game.get_all_players_ids()
            for id in ids:
                self.set_player_name(id, str(id))
        else:
            for id in player_names:
                if self.game.has_player(id):
                    self.set_player_name(id, player_names[id])
            return

    def set_player_name(self, player_id, player_name: str):
        self.player_names_dict[player_id] = player_name[:DiscordCardGame.PLAYER_NAME_MAX_LENGTH]