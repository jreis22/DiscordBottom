from typing import List
from card_game_logic.card_games.card_game_type import CardGameType
from card_game_logic.card_games.card_game import CardGame
from card_game_logic.card_games.bisca import Bisca
from card_game_logic.card_games.sueca import Sueca
from card_game_logic.player import CardPlayer

class CardGameFactory:
    def __init__(self):
        pass

    def create(self, game_type: CardGameType, players: List[CardPlayer], challenger_id=None) -> CardGame:
        if game_type == CardGameType.BISCA:
            return Bisca(players=players, first_player_id=challenger_id)

        if game_type == CardGameType.SUECA:
            return Sueca(players=players, first_player_id=challenger_id)
            
        return None
