import unittest
import sys
from tests_config import TEST_CONFIG
sys.path.insert(
    1, TEST_CONFIG['SRC_PATH'])
from card_game_logic.cards.card_enums import Rank, Suit

class CardEnumTest(unittest.TestCase):

    def test_eq(self):
        obj = Suit.SPADES
        obj2 = Suit.SPADES
        self.assertEqual(obj, obj2)
        self.assertTrue(obj == obj2)

        obj2 = Suit.HEARTS
        self.assertNotEqual(obj, obj2)

    def test_suit_get_all(self):
        result = Suit.get_all()
        expected_result = [Suit.HEARTS, Suit.SPADES, Suit.CLUBS, Suit.DIAMONDS]

        for expected in expected_result:
            self.assertTrue(result.__contains__(expected))

    def test_rank_eq(self):
        obj1 = Rank.ACE
        obj2 = Rank.ACE

        self.assertTrue(obj1 == obj2)

        obj2 = Rank.EIGHT
        self.assertTrue(obj1 != obj2)

        self.assertTrue(obj1 < obj2)


if __name__ == '__main__':
    unittest.main()
