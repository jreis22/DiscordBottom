import unittest
import sys
sys.path.insert(
    1, '/Users/joao reis/Documents/projects/Discord/Bots/DiscordBottom/DiscordBottom/src')
from card_game_logic.cards.card_deck import CardDeck
from card_game_logic.cards.card import PlayingCard
from card_game_logic.cards.card_enums import Rank, Suit, DeckFormat
from card_game_logic.cards.card_hand import CardHand
from card_game_logic.player import CardPlayer
from card_game_logic.card_games.card_game import CardGame

class CardGameTest(unittest.TestCase):

    def setUp(self):
        self.player = CardPlayer(player_id=1,card_hand=CardHand())

        self.card_list = [PlayingCard(suit=Suit.SPADES, rank=Rank.TEN), PlayingCard(
            suit=Suit.DIAMONDS, rank=Rank.JACK), PlayingCard(suit=Suit.CLUBS, rank=Rank.EIGHT)]

    def test_number_of_cards_left(self):
        self.player.deal_cards(self.card_list)
        self.assertTrue(self.player.number_of_cards_left() == 3)

    def test_has_cards(self):
        self.assertFalse(self.player.has_cards())
        self.player.deal_cards(self.card_list)
        self.assertTrue(self.player.has_cards())

if __name__ == '__main__':
    unittest.main()
