import unittest
import sys
sys.path.insert(
    1, '/Users/joao reis/Documents/projects/Discord/Bots/DiscordBottom/DiscordBottom/src')
from card_game_logic.card_games.card_game import CardGame
from card_game_logic.player import CardPlayer
from card_game_logic.cards.card_hand import CardHand
from card_game_logic.cards.card_enums import Rank, Suit, DeckFormat
from card_game_logic.cards.card import PlayingCard
from card_game_logic.cards.card_deck import CardDeck
from card_game_logic.card_games.played_card import PlayedCard


class CardGameTest(unittest.TestCase):

    def setUp(self):
        players_dict = [CardPlayer(1),
                        CardPlayer(2),
                        CardPlayer(3),
                        CardPlayer(4)]
        player_order = [1, 2, 3, 4]

        self.game = CardGame(cards_per_player=7, players=players_dict,
                             player_order=player_order, card_deck=CardDeck(DeckFormat.FIFTY_TWO))
        self.game.card_deck.build_deck()

    def test_CardGame_constructor(self):
        self.assertTrue(self.game.cards_per_player == 7)
        self.assertTrue(len(self.game.players) == 4)
        self.assertTrue(self.game.card_deck.list_size() == 52)

    def test_get_player_cards(self):
        try:
            self.game.get_player_cards(0)
        except Exception:
            pass
        else:
            self.fail(
                "game.getplayercards out of index did not raise expected error")

        self.assertEqual([], self.game.get_player_cards(1))
        expected = [
            PlayingCard(suit=Suit.CLUBS, rank=Rank.ACE),
            PlayingCard(suit=Suit.SPADES, rank=Rank.FIVE)
        ]
        self.game.players[1].set_card_hand(CardHand(expected))
        unexpected = [PlayingCard(suit=Suit.CLUBS, rank=Rank.ACE), PlayingCard(suit=Suit.SPADES, rank=Rank.ACE)]
        self.assertEqual(self.game.get_player_cards(1), expected)
        self.assertNotEqual(self.game.get_player_cards(1), unexpected)
        
    def test_deal_cards(self):
        self.game.deal_cards()

        # loop players
        for player in self.game.players:
            # assert right numer of cards for player
            self.assertTrue(
                self.game.players[player].card_hand.list_size() == self.game.cards_per_player)

            # loop player cards
            for card in self.game.players[player].card_hand.show_cards():
                # assert card isnt in game deck
                self.assertFalse(self.game.card_deck.contains_card(card))

                # check if other players dont have same cards
                for player2 in self.game.players:
                    if player2 != player:
                        self.assertFalse(
                            self.game.players[player2].card_hand.contains_card(card))

        # assert number of cards left in deck
        self.assertTrue(self.game.card_deck.list_size() == 52 -
                        (len(self.game.players)*self.game.cards_per_player))

    def test_rotate_player_order(self):
        self.game.rotate_player_order()
        expected = [2, 3, 4, 1]
        self.assertEqual(self.game.player_order, expected)

        self.game.inverse_rotate_player_order()
        expected = [1, 2, 3, 4]
        self.assertEqual(self.game.player_order, expected)

    def test_rotate_player_order_n_times(self):
        self.game.rotate_player_order_n_times(2)
        expected = [3, 4, 1, 2]
        self.assertEqual(self.game.player_order, expected)

        self.game.inverse_rotate_player_order_n_times(3)
        expected = [4, 1, 2, 3]
        self.assertEqual(self.game.player_order, expected)
        self.game.inverse_rotate_player_order_n_times(1)
        expected = [3, 4, 1, 2]
        self.assertEqual(self.game.player_order, expected)

        self.game.rotate_player_order_n_times(4)
        self.assertEqual(self.game.player_order, expected)

    def test_start_game(self):
        self.game.card_deck = CardDeck(DeckFormat.FIFTY_TWO)
        self.game.start_game()
        self.assertTrue(
            self.game.players[1].number_of_cards_left() == self.game.cards_per_player)
        self.assertTrue(self.game.card_deck.list_size() == 52 - (7 * 4))
        self.assertFalse(
            self.game.players[1].card_hand == self.game.players[2].card_hand)

    def test_add_played_card(self):
        self.game.add_played_card(player_key=1, card=PlayingCard(suit=Suit.HEARTS, rank=Rank.FOUR), game_round=1)
        self.game.add_played_card(player_key=2, card=PlayingCard(suit=Suit.DIAMONDS, rank=Rank.TWO), game_round=1)
        self.game.add_played_card(player_key=1, card=PlayingCard(suit=Suit.SPADES, rank=Rank.QUEEN), game_round=2)
        self.game.add_played_card(player_key=2, card=PlayingCard(suit=Suit.CLUBS, rank=Rank.JACK), game_round=2)

        self.assertTrue(self.game.played_cards.__contains__(PlayedCard(player_key=1, card=PlayingCard(suit=Suit.HEARTS, rank=Rank.FOUR), game_round=1)))
        self.assertTrue(self.game.played_cards.__contains__(PlayedCard(player_key=1, card=PlayingCard(suit=Suit.SPADES, rank=Rank.QUEEN), game_round=2)))
        self.assertTrue(self.game.played_cards.__contains__(PlayedCard(player_key=2, card=PlayingCard(suit=Suit.DIAMONDS, rank=Rank.TWO), game_round=1)))
        self.assertFalse(self.game.played_cards.__contains__(PlayedCard(player_key=1, card=PlayingCard(suit=Suit.HEARTS, rank=Rank.FOUR), game_round=2)))

    def test_set_all_players_playing(self):
        for player in self.game.players.values():
            player.pass_turn()

        self.game.set_all_players_playing()
        count = 0
        for player in self.game.players.values():
            self.assertTrue(player.is_playing())
            count+=1

        self.assertTrue(count == 4)

    def test_get_plays_from_round(self):
        self.game.add_played_card(player_key=1, card=PlayingCard(suit=Suit.HEARTS, rank=Rank.FOUR), game_round=1)
        self.game.add_played_card(player_key=2, card=PlayingCard(suit=Suit.DIAMONDS, rank=Rank.TWO), game_round=1)
        self.game.add_played_card(player_key=1, card=PlayingCard(suit=Suit.SPADES, rank=Rank.QUEEN), game_round=2)
        self.game.add_played_card(player_key=2, card=PlayingCard(suit=Suit.CLUBS, rank=Rank.JACK), game_round=2)

        result = self.game.get_plays_from_round(1)
        expected = [
            PlayedCard(player_key=1, card=PlayingCard(suit=Suit.HEARTS, rank=Rank.FOUR), game_round=1),
            PlayedCard(player_key=2, card=PlayingCard(suit=Suit.DIAMONDS, rank=Rank.TWO), game_round=1),
        ]
        self.assertEqual(result, expected)
        
if __name__ == '__main__':
    unittest.main()
