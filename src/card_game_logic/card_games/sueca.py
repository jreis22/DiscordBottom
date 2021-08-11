from typing import List
from card_game_logic.card_games.game_state import GameStateEnum
from card_game_logic.card_games.played_card import PlayedCard
from card_game_logic.card_games.trick_taking_game import TrickTakingGame
from card_game_logic.card_games.card_values_enum import CardValuesEnum
from card_game_logic.cards.card import PlayingCard
from card_game_logic.cards.card_deck import CardDeck
from card_game_logic.cards.card_enums import DeckFormat
from card_game_logic.cards.card_enums import Suit


class Sueca(TrickTakingGame):

    def __init__(self, players: dict, current_suit: Suit = Suit.JOKER,
                 trump_suit: Suit = Suit.JOKER,
                 current_round: int = 1, card_deck: CardDeck = None,
                 player_order: list = None, first_player_id=None, played_cards: List[PlayedCard] = None, game_state: GameStateEnum = GameStateEnum.CREATED):

        if len(players) != 4:
            raise Exception("Must have 2 players to start game")

        super().__init__(cards_per_player=10, card_deck=card_deck, current_round=current_round, players=players, game_state=game_state,
                         player_order=player_order, first_player_id=first_player_id, played_cards=played_cards)

        self.current_suit = current_suit
        self.trump_suit = trump_suit

    # override
   # def start_game(self):
    #    CardGame.start_game(self)
     #   self.current_round = 1

    def get_default_deck(self) -> CardDeck:
        return CardDeck(DeckFormat.FORTY)

    def get_rank_dictionary(self) -> CardValuesEnum:
        return CardValuesEnum.ACE_SEVEN.value
    
    def start_game(self):
        self.card_deck.build_deck()
        self.card_deck.shuffle()
        self.last_card = self.card_deck.get_last_card()
        self.trump_suit = self.last_card.suit
        self.deal_cards()
        self.order_players()
        self.last_card_owner = None
        for player_id in self.player_order:
            if self.player_has_card(player_id=player_id, suit=self.last_card.suit, rank=self.last_card.rank):
                self.last_card_owner = player_id
                break
        self.game_state = GameStateEnum.STARTED
    
    def get_last_card_owner(self):
        return self.last_card_owner

    def get_last_card(self) -> PlayingCard:
        return self.last_card