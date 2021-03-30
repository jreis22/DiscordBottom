import unittest
import sys
sys.path.insert(1, '/Users/joao reis/Documents/projects/Discord/Bots/DiscordBottom/DiscordBottom/src')
from card_game_logic.cards.card import PlayingCard
from card_game_logic.cards.card_enums import Rank, Suit



class CardTest(unittest.TestCase):


    def test_card_constructor(self):
        card = PlayingCard(suit=Suit.SPADES, rank=Rank.SEVEN)
         
        self.assertEqual(card.suit, Suit.SPADES)

    def test_eq(self):
        obj = PlayingCard(suit=Suit.SPADES, rank=Rank.SEVEN)
        expected_true = PlayingCard(suit=Suit.SPADES, rank=Rank.SEVEN)
        diff_suit = PlayingCard(suit=Suit.HEARTS, rank=Rank.SEVEN)
        diff_rank = PlayingCard(suit=Suit.SPADES, rank=Rank.KING)

        self.assertEqual(obj, expected_true)
        self.assertFalse(obj == diff_suit)
        self.assertFalse(obj == diff_rank)

if __name__ == '__main__':
    unittest.main()
