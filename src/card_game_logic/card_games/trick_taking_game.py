from card_game_logic.card_games.card_game import CardGame
from card_game_logic.card_games.game_state import GameStateEnum
from card_game_logic.card_games.card_values_enum import CardValuesEnum
from card_game_logic.player import CardPlayer
from card_game_logic.cards.card_enums import Suit, Rank
from card_game_logic.cards.card_deck import CardDeck
from card_game_logic.cards.card import PlayingCard

#base trick taking game, most rules are based on sueca
class TrickTakingGame(CardGame):

    # in trick take, the round is a trick
    def __init__(self, players: dict, cards_per_player: int, current_suit: Suit = Suit.JOKER,
                 trump_suit: Suit = Suit.JOKER,
                 current_round: int = 1, card_deck: CardDeck = None,
                 player_order: [] = None, played_cards: [] = None, game_state: GameStateEnum = GameStateEnum.CREATED):
        super().__init__(cards_per_player=cards_per_player, card_deck=card_deck, players=players, game_state=game_state,
                         player_order=player_order, played_cards=played_cards)

        self.current_suit = current_suit
        self.trump_suit = trump_suit
        self.current_round = current_round

    # point dict is a dictionary that specifies the value of different card ranks
    def play_card(self, player_key, card: PlayingCard):
        player = self.players[player_key]

        self.validate_player(player=player, card=card)
        self.validate_card_suit(player=player, card=card)
        self.validate_card_rank(player=player, card=card)

        self._play_card(player=player, card=card)
        self._after_play_card_routine()
    # -------play validation--------
    # default validation for player in method play_card method

    def validate_player(self, player: CardPlayer, card: PlayingCard):
        if not player.is_playing():
            raise Exception(f'Player {player.player_id} cant play')
        if self.player_order[0] != player.player_id:
            raise Exception(f"It's not {player.player_id}'s turn")
        if not player.has_card(card):
            raise Exception(
                f"Player {player.player_id} doesn't own card {card}")

    # validation of card suit played in method play_card
    def validate_card_suit(self, player: CardPlayer, card: PlayingCard):
        if not self.card_is_from_current_suit(card):
            if self.current_suit == Suit.JOKER:
                self.change_follow_suit(card.suit)
            elif player.contains_card_of_suit(self.current_suit):
                raise Exception(
                    f"Player {player.player_id} must play card of current round suit {self.current_suit}")

    # card rank validation called by play_card method
    # default does not validate rank (probably usefull for climbing card games)
    def validate_card_rank(self, player: CardPlayer, card: PlayingCard):
        pass

    def card_is_from_current_suit(self, card: PlayingCard) -> bool:
        return card.suit == self.current_suit

    # in case games decide to override function so suit doesnt change or to make further validations
    def change_follow_suit(self, suit: Suit):
        self.current_suit = suit

    # -------play--------

    # function called by play_card method that executes the routine of playing a card (may change from game to game)
    def _play_card(self, player: CardPlayer, card: PlayingCard):
        player.play_card(card)
        self.add_played_card(player_key=player.player_id,
                             card=card, round=self.current_round)
        self.player_state_change_after_play(player)
    
    #state the player is left in after sucessfully playing a card
    def player_state_change_after_play(self, player):
        player.pass_turn()

    # routines done after played card has been accepted and transaction has ended
    # default rotates the order of the players and checks for round/game end
    def _after_play_card_routine(self):
        self.rotate_player_order()
        if self.end_round():
            self.end_game()

    # end round called by play_card to check if round is over

    def end_round(self) -> bool:
        if self.exists_players_playing():
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
        return True
    # end game called by play_card to check if game is over

    def end_game(self) -> bool:
        if self.current_round == 21:
            self.game_state = GameStateEnum.GAME_END

    # method assumes played cards array is ordered
    def get_round_winner(self, current_round):
        plays = self.get_plays_from_round(current_round)
        best_play = plays[0]
        round_suit = best_play.card.suit
        for play in plays[1:]:
            card1 = best_play.card
            card2 = play.card
            if self.compare_cards(card1=card1, card2=card2, round_suit=round_suit) == card2:
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
