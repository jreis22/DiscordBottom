from typing import List
from card_game_logic.cards.card_list import CardList
from card_game_logic.cards.card_enums import DeckFormat, Rank, Suit
from card_game_logic.cards.card import PlayingCard

class CardDeck(CardList):

    def __init__(self, deck_format: DeckFormat = DeckFormat.FIFTY_TWO):
        super().__init__()
        self.deck_format = deck_format

    def build_deck(self):
        self.add_cards(DeckBuilder.build_deck(self.deck_format))


class DeckBuilder:
    @staticmethod
    def build_deck(deck_format: DeckFormat) -> List[PlayingCard]:
        if deck_format == DeckFormat.FORTY:
            deck = DeckBuilder.__build_40_card_deck__()
            return deck
        elif deck_format == DeckFormat.FIFTY_TWO:
            return DeckBuilder.__build_52_card_deck__()
        elif deck_format == DeckFormat.FIFTY_FOUR:
            return DeckBuilder.__build_54_card_deck__()

    @staticmethod
    def __build_40_card_deck__() -> List[PlayingCard]:
        ranks = Rank.get_pip_ranks()[0:7] + Rank.get_court_ranks()

        return DeckBuilder.__create_cards_for_each_suit__(ranks)

    @staticmethod
    def __build_52_card_deck__() -> List[PlayingCard]:
        ranks = Rank.get_pip_ranks() + Rank.get_court_ranks()

        return DeckBuilder.__create_cards_for_each_suit__(ranks)

    @staticmethod
    def __build_54_card_deck__() -> List[PlayingCard]:
        ranks = Rank.get_pip_ranks() + Rank.get_court_ranks() + \
            ([Rank.JOKER]*2)

        return DeckBuilder.__create_cards_for_each_suit__(ranks)

    @staticmethod
    def __create_cards_for_each_suit__(ranks: List[Rank]) -> List[PlayingCard]:
        suits = Suit.get_all()
        deck = []
        for rank in ranks:
            if rank != Rank.JOKER:
                for suit in suits:
                    deck.append(PlayingCard(rank=rank, suit=suit))
            else:
                deck.append(PlayingCard(suit=Suit.JOKER, rank=Rank.JOKER))

        return deck
            
# deck = CardDeck(DeckFormat.FORTY)
# deck.__print_list__()
# print('dealt cards: ')
# for card in deck.dean_n_cards(3):
#     print(card)

# print('deck: ')
# deck.__print_deck__()