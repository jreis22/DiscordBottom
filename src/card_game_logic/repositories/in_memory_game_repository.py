import copy
from card_game_logic.repositories.game_repository import GameRepository
from card_game_logic.card_games.card_game import CardGame

class InMemoryGameRepository(GameRepository):

    def __init__(self):
        self.games = {}

    def get_by_id(self, game_id) -> CardGame:
        return copy.deepcopy(self.games[game_id])

    def insert(self, game: CardGame) -> bool:
        self.games[game.get_id()] = game
        return True
    
    def update(self, game_id, game: CardGame) -> bool:
        self.games[game_id] = game
        return True
        
    def has(self, game_id) -> bool:
        return self.games.keys().__contains__(game_id)
    