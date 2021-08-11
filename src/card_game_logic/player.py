from typing import List
from card_game_logic.cards.card_hand import CardHand
from card_game_logic.player_state import PlayerStateEnum
from card_game_logic.cards.card import PlayingCard
from card_game_logic.cards.card_enums import Rank, Suit

# player that participates in a card game


class CardPlayer:
    def __init__(self, player_id, player_name: str = None, team: int = 0, card_hand: CardHand = None, player_state: PlayerStateEnum = PlayerStateEnum.PENDING, points: int = 0):
        self.player_id = player_id
        self.set_player_name(player_name)
        self.set_card_hand(card_hand)
        self.player_state = player_state
        self.points = points
        self.team = team

    def get_player_name(self) -> str:
        return self.player_name

    def set_player_name(self, player_name: str):
        if player_name is None:
            if self.player_id is None:
                self.player_name = ""
            else:
                self.player_name = str(self.player_id)
        else:
            self.player_name = player_name

    def set_card_hand(self, new_card_hand: CardHand):
        if new_card_hand is None:
            self.card_hand = CardHand()
        else:
            self.card_hand = new_card_hand

    def set_card_hand_with_list(self, card_list: List[PlayingCard]):
        if card_list is None:
            self.card_hand = CardHand()
        else:
            self.card_hand = CardHand(card_list=card_list)

    def order_card_hand(self):
        self.card_hand.sort_by_suit()

    def show_hand(self) -> List[PlayingCard]:
        return self.card_hand.show_cards()

    def number_of_cards_left(self) -> int:
        return self.card_hand.list_size()

    def has_cards(self) -> bool:
        return not self.card_hand.is_empty()

    def deal_cards(self, card_hand: List[PlayingCard]):
        self.card_hand.add_cards(card_hand)
        self.order_card_hand()

    def deal_card(self, card: PlayingCard):
        self.card_hand.add_card(card)
        self.order_card_hand()

    def add_points(self, points: int) -> int:
        self.points += points
        return self.points

    def subtract_points(self, points: int) -> int:
        self.points -= points
        return self.points

    def current_points(self) -> int:
        return self.points

    def quit(self):
        self.player_state = PlayerStateEnum.QUIT

    def play_card(self, card: PlayingCard) -> bool:
        return self.card_hand.remove_card(card)

    def has_card(self, card: PlayingCard) -> bool:
        return self.card_hand.contains_card(card)

    def contains_card_of_suit(self, suit: Suit) -> bool:
        return self.card_hand.contains_card_of_suit(suit)

    def contains_card_of_rank(self, rank: Rank) -> bool:
        return self.card_hand.contains_card_of_rank(rank)

    def is_playing(self) -> bool:
        return self.player_state == PlayerStateEnum.PLAYING

    def is_quitting(self) -> bool:
        return self.player_state == PlayerStateEnum.QUIT

    def is_pending(self) -> bool:
        return self.player_state == PlayerStateEnum.PENDING


    def set_state_playing(self):
        self.player_state = PlayerStateEnum.PLAYING

    def pass_turn(self):
        self.player_state = PlayerStateEnum.PASS

    def __eq__(self, other) -> bool:
        if isinstance(other, CardPlayer):
            return self.player_id == other.player_id
        return False