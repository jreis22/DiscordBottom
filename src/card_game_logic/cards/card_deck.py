
from card_game_logic.cards.card_list import CardList
from card_game_logic.cards.card_enums import DeckFormat
from card_game_logic.cards.default_deck_builder import DeckBuilder


class CardDeck(CardList):

    def __init__(self, deck_format: DeckFormat = DeckFormat.FIFTY_TWO):
        super().__init__()
        self.deck_format = deck_format

    def build_deck(self):
        self.add_cards(DeckBuilder.build_deck(self.deck_format))

            
# deck = CardDeck(DeckFormat.FORTY)
# deck.__print_list__()
# print('dealt cards: ')
# for card in deck.dean_n_cards(3):
#     print(card)

# print('deck: ')
# deck.__print_deck__()