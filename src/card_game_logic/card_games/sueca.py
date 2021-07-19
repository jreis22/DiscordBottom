from card_game_logic.card_games.game_state import GameStateEnum
from card_game_logic.card_games.trick_taking_game import TrickTakingGame
from card_game_logic.card_games.card_values_enum import CardValuesEnum
from card_game_logic.cards.card_deck import CardDeck
from card_game_logic.cards.card_enums import DeckFormat
from card_game_logic.cards.card_enums import Suit


class Sueca(TrickTakingGame):

    def __init__(self, players: dict, current_suit: Suit = Suit.JOKER,
                 trump_suit: Suit = Suit.JOKER,
                 current_round: int = 1, card_deck: CardDeck = None,
                 player_order: [] = None, first_player_id=None, played_cards: [] = None, game_state: GameStateEnum = GameStateEnum.CREATED):

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
