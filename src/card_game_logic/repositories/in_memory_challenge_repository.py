import copy
from card_game_logic.repositories.challenge_repository import CardGameChallengeRepository
from card_game_logic.card_games.card_game_challenge import CardGameChallenge

class InMemoryChallengeRepository(CardGameChallengeRepository):

    def __init__(self):
        self.challenges = {}

    def get_by_id(self, challenge_id) -> CardGameChallenge:
        if self.has(challenge_id=challenge_id):
            return copy.copy(self.challenges[challenge_id])
        else:
            return None

    def insert(self, challenge: CardGameChallenge) -> bool:
        self.challenges[challenge.get_id()] = challenge
        return True
    
    def update(self, challenge_id, challenge: CardGameChallenge) -> bool:
        self.challenges[challenge_id] = challenge
        return True
        
    def has(self, challenge_id) -> bool:
        return self.challenges.keys().__contains__(challenge_id)

    def get_last_n_entries(self, n: int):
        length = len(self.challenges)
        if n > length:
            n = length
        
        arr = self.challenges.values()

        return list(arr)[length-n:]