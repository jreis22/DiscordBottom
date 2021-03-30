from card_game_logic.cards.card import PlayingCard


class PlayedCard:
    def __init__(self, player_key, card: PlayingCard, game_round: int):
        self.player_key = player_key
        self.card = card
        self.round = game_round

    def __eq__(self, other):
        if isinstance(other, PlayedCard):
            return other.player_key == self.player_key and self.card == other.card and self.round == other.round
        else:
            return False
