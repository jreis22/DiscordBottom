
from card_game_logic.card_games.card_game_challenge import CardGameChallenge
from card_game_logic.repositories.base_repository import BaseRepository

class CardGameChallengeRepository(BaseRepository):

    def get_last_n_entries(self, n: int):
        pass