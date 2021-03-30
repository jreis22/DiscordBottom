from typing import List
from card_game_logic.cards.card_list import CardList
from card_game_logic.cards.card import PlayingCard

class CardHand(CardList):

    def __init__(self, card_list: List[PlayingCard] = None):
        super().__init__(card_list=card_list)

