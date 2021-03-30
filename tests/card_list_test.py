import unittest
import sys
sys.path.insert(
    1, '/Users/joao reis/Documents/projects/Discord/Bots/DiscordBottom/DiscordBottom/src/')
from card_game_logic.cards.card import PlayingCard
from card_game_logic.cards.card_enums import Rank, Suit
from card_game_logic.cards.card_list import CardList


class CardListTest(unittest.TestCase):

    def setUp(self):
        self.list1 = [PlayingCard(suit=Suit.SPADES, rank=Rank.TEN), PlayingCard(
            suit=Suit.DIAMONDS, rank=Rank.JACK), PlayingCard(suit=Suit.CLUBS, rank=Rank.EIGHT)]
        self.cardl = CardList(card_list=self.list1)

    def test_card_list_constructor(self):
        cardL = CardList()
        self.assertEqual(len(cardL.show_cards()), 0)

        cardL = CardList([PlayingCard(suit=Suit.SPADES, rank=Rank.FIVE)])
        expected_list = [PlayingCard(suit=Suit.SPADES, rank=Rank.FIVE)]

        self.assertEqual(len(cardL.show_cards()), len(expected_list))
        self.assertEqual(cardL.show_cards()[0], expected_list[0])

    def test_show_cards(self):
        size = len(self.list1)
        for i in range(size):
            self.assertEqual(self.list1[i], self.cardl.show_cards()[i])

    def test_similar(self):
        list2 = [PlayingCard(suit=Suit.DIAMONDS, rank=Rank.JACK), PlayingCard(
            suit=Suit.SPADES, rank=Rank.TEN), PlayingCard(suit=Suit.CLUBS, rank=Rank.EIGHT)]

        cardl2 = CardList(list2)

        self.assertTrue(self.cardl.similar(cardl2))

        list2 = [PlayingCard(suit=Suit.HEARTS, rank=Rank.JACK), PlayingCard(
            suit=Suit.SPADES, rank=Rank.TEN), PlayingCard(suit=Suit.CLUBS, rank=Rank.EIGHT)]
        cardl2 = CardList(list2)
        self.assertFalse(self.cardl.similar(cardl2))

    def test_eq(self):
        list2 = [PlayingCard(suit=Suit.DIAMONDS, rank=Rank.JACK), PlayingCard(
            suit=Suit.SPADES, rank=Rank.TEN), PlayingCard(suit=Suit.CLUBS, rank=Rank.EIGHT)]

        cardl2 = CardList(list2)

        self.assertFalse(self.cardl == cardl2)

        list2 = [PlayingCard(suit=Suit.SPADES, rank=Rank.TEN), PlayingCard(
            suit=Suit.DIAMONDS, rank=Rank.JACK), PlayingCard(suit=Suit.CLUBS, rank=Rank.EIGHT)]
        cardl2 = CardList(list2)
        self.assertTrue(self.cardl == cardl2)

    def test_size(self):
        expected = 3
        result = self.cardl.list_size()

        self.assertEqual(expected, result)

    def test_contains_card(self):
        card1 = PlayingCard(suit=Suit.SPADES, rank=Rank.TEN)

        self.assertTrue(self.cardl.contains_card(card1))

        card1 = PlayingCard(suit=Suit.SPADES, rank=Rank.THREE)
        self.assertFalse(self.cardl.contains_card(card1))

    def test_contains_card_of_suit(self):
        self.assertFalse(self.cardl.contains_card_of_suit(Suit.HEARTS))
        self.assertTrue(self.cardl.contains_card_of_suit(Suit.CLUBS))
        self.assertTrue(self.cardl.contains_card_of_suit(Suit.SPADES))
        self.assertTrue(self.cardl.contains_card_of_suit(Suit.DIAMONDS))

    def test_contains_card_of_rank(self):
        self.assertFalse(self.cardl.contains_card_of_rank(Rank.ACE))
        self.assertTrue(self.cardl.contains_card_of_rank(Rank.TEN))
        self.assertTrue(self.cardl.contains_card_of_rank(Rank.JACK))
        self.assertTrue(self.cardl.contains_card_of_rank(Rank.EIGHT))

    def test_deal_card(self):
        expected = PlayingCard(suit=Suit.SPADES, rank=Rank.TEN)
        result = self.cardl.deal_card()
        self.assertEqual(result, expected)

        list2 = [PlayingCard(
            suit=Suit.DIAMONDS, rank=Rank.JACK), PlayingCard(suit=Suit.CLUBS, rank=Rank.EIGHT)]
        self.assertEqual(self.cardl.show_cards(), list2)

    def test_deal_n_cards(self):
        expected = [PlayingCard(suit=Suit.SPADES, rank=Rank.TEN), PlayingCard(
            suit=Suit.DIAMONDS, rank=Rank.JACK)]
        result = self.cardl.deal_n_cards(2)

        self.assertEqual(result, expected)

        list2 = [PlayingCard(suit=Suit.CLUBS, rank=Rank.EIGHT)]
        self.assertEqual(self.cardl.show_cards(), list2)

    def test_add_card(self):
        cardl = CardList()
        card = PlayingCard(suit=Suit.SPADES, rank=Rank.QUEEN)
        cardl.add_card(card)

        self.assertTrue(cardl.list_size() == 1)

    def test_add_cards(self):
        card = PlayingCard(suit=Suit.SPADES, rank=Rank.QUEEN)
        card2 = PlayingCard(suit=Suit.HEARTS, rank=Rank.FOUR)
        card3 = PlayingCard(suit=Suit.CLUBS, rank=Rank.KING)

        cardl = CardList()
        cardl.add_cards([card, card2])
        expected = [card, card2]
        result = cardl.show_cards()
        self.assertEqual(result, expected)

        cardl = CardList([card3])
        cardl.add_cards([card, card2])
        result = cardl.show_cards()
        self.assertNotEqual(result, expected)
        expected = [card3, card, card2]
        self.assertEqual(result, expected)

    def test_sort_by_rank(self):
        expected_list = [PlayingCard(suit=Suit.CLUBS, rank=Rank.EIGHT),
                         PlayingCard(suit=Suit.SPADES, rank=Rank.TEN), PlayingCard(
            suit=Suit.DIAMONDS, rank=Rank.JACK)]
        expected = CardList(expected_list)
        self.cardl.sort_by_rank()
        self.assertEqual(expected, self.cardl)

    def test_sort_by_suit(self):
        expected_list = [
            PlayingCard(suit=Suit.DIAMONDS, rank=Rank.TWO),
            PlayingCard(suit=Suit.DIAMONDS, rank=Rank.JACK),
            PlayingCard(suit=Suit.CLUBS, rank=Rank.EIGHT),
            PlayingCard(suit=Suit.SPADES, rank=Rank.TEN)
        ]
        expected = CardList(expected_list)

        self.cardl.add_card(PlayingCard(suit=Suit.DIAMONDS, rank=Rank.TWO))
        self.cardl.sort_by_suit()
        self.assertTrue(expected == self.cardl)

    def test_is_empty(self):
        self.assertFalse(self.cardl.is_empty())

        cardl2 = CardList()
        self.assertTrue(cardl2.is_empty())


if __name__ == '__main__':
    unittest.main()
