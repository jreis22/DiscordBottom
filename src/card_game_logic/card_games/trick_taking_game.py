from typing import List
from card_game_logic.card_games.card_game import CardGame
from card_game_logic.card_games.game_state import GameStateEnum
from card_game_logic.card_games.card_values_enum import CardValuesEnum
from card_game_logic.player import CardPlayer
from card_game_logic.cards.card_enums import Suit, Rank
from card_game_logic.cards.card_deck import CardDeck
from card_game_logic.cards.card import PlayingCard
from card_game_logic.card_games.played_card import PlayedCard

#base trick taking game, most rules are based on sueca
class TrickTakingGame(CardGame):

    # in trick take, the round is a trick
    def __init__(self, players: List[CardPlayer], cards_per_player: int, current_suit: Suit = Suit.JOKER,
                 trump_suit: Suit = Suit.JOKER,
                 current_round: int = 1, card_deck: CardDeck = None,
                 player_order: List[CardPlayer] = None, played_cards: List[PlayedCard] = None, game_state: GameStateEnum = GameStateEnum.CREATED):
        super().__init__(cards_per_player=cards_per_player, card_deck=card_deck, players=players, game_state=game_state,
                         player_order=player_order, played_cards=played_cards)

        self.current_suit = current_suit
        self.trump_suit = trump_suit
        self.current_round = current_round

    def _play_card(self, player: CardPlayer, card: PlayingCard):
        
        if self.is_round_start():
            self.change_follow_suit(card.suit)
            self.set_state_playing_phase()
        super()._play_card(player=player, card=card)

    # -------play validation--------
    # default validation for player in method play_card method
    def is_card_valid(self, player: CardPlayer, card: PlayingCard) -> bool:
        return self.is_round_start() or (self.is_card_suit_valid(player=player, card=card) and self.is_card_rank_valid(player=player, card=card))

    # validation of card suit played in method play_card
    def is_card_suit_valid(self, player: CardPlayer, card: PlayingCard) -> bool:
        if not self.card_is_from_current_suit(card):
            if player.contains_card_of_suit(self.current_suit):
                return False
        return True

    def card_is_from_current_suit(self, card: PlayingCard) -> bool:
        return card.suit == self.current_suit

    # in case games decide to override function so suit doesnt change or to make further validations
    def change_follow_suit(self, suit: Suit):
        self.current_suit = suit

    # -------play--------
    #

    #state the player is left in after sucessfully playing a card
    def player_state_change_after_play(self, player):
        player.pass_turn()

    # end round called by play_card to check if round is over
    def end_round(self) -> bool:
        if not self.can_round_end():
            return False

        winner = self.get_round_winner(self.current_round)
        self.players[winner].add_points(
            self.get_round_points(self.current_round))

        if self.player_order[0] != winner:
            winner_index = self.player_order.index(
                winner, 1, len(self.player_order))
            self.rotate_player_order_n_times(winner_index)
        self.current_round += 1
        self.set_all_players_playing()
        if self.card_deck.list_size() > 0:
            for player in self.players:
                self.deal_n_cards_to_player(player_key=player, nCards=1)

        self.current_suit = Suit.JOKER
        self.set_state_round_start()
        return True
    
    # method assumes played cards array is ordered
    def get_round_winner(self, current_round) -> PlayedCard:
        plays = self.get_plays_from_round(current_round)
        best_play = plays[0]
        round_suit = best_play.card.suit
        for play in plays[1:]:
            card2 = play.card
            if self.compare_cards(card1=best_play.card, card2=card2, round_suit=round_suit) == card2:
                best_play = play

        return best_play.player_key

    def get_round_points(self, current_round) -> int:
        plays = self.get_plays_from_round(current_round)
        points = 0
        point_dict = self.get_rank_dictionary() 
        for play in plays:
            if point_dict.__contains__(play.card.rank.value):
                points += point_dict[play.card.rank.value]

        return points

    def compare_cards(self, card1: PlayingCard, card2: PlayingCard, round_suit: Suit) -> PlayingCard:
        if card1.suit == card2.suit:
            return self.rank_comparison(card1, card2)
        elif card1.suit == self.trump_suit:
            return card1
        elif card2.suit == self.trump_suit:
            return card2
        elif card1.suit == round_suit:
            return card1
        elif card2.suit == round_suit:
            return card2
        else:
            return None

    def rank_comparison(self, card1: PlayingCard, card2: PlayingCard) -> PlayingCard:
        rank1 = card1.rank
        rank2 = card2.rank
        rank_dictionary = self.get_rank_dictionary()
        if rank1 == rank2:
            return None
        elif rank_dictionary.__contains__(rank1.value):
            if rank_dictionary.__contains__(rank2.value)\
               and rank_dictionary[rank1.value] < rank_dictionary[rank2.value]:
                return card2
            else:
                return card1

        elif (rank_dictionary.__contains__(rank2.value)):
            return card2
        else:
            if rank1 > rank2:
                return card1
            else:
                return card2

    #override this method for rank comparison in different games
    def get_rank_dictionary(self) -> CardValuesEnum:
        return CardValuesEnum.ACE_TEN.value
