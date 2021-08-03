import uuid
from typing import List

from card_game_logic.player import CardPlayer
from card_game_logic.cards.card_deck import CardDeck
from card_game_logic.cards.card_enums import DeckFormat
from card_game_logic.card_games.game_state import GameStateEnum
from card_game_logic.cards.card import PlayingCard
from card_game_logic.card_games.played_card import PlayedCard


class CardGame():

    # rounds are
    def __init__(self, cards_per_player: int, current_round: int = 1, game_id: uuid.UUID = None, players: List[CardPlayer] = None,
                 card_deck: CardDeck = None,
                 game_state: GameStateEnum = GameStateEnum.CREATED,
                 player_order: list = None, first_player_id = None, played_cards: List[PlayedCard] = None):
        self.set_players(players)
        self.set_card_deck(card_deck)
        self.game_state = game_state
        self.cards_per_player = cards_per_player
        self.set_player_order(player_order)
        self.set_played_cards(played_cards)
        self._set_id_(game_id)
        self.current_round = current_round
        self.first_player_id = first_player_id

    # setters & getters

    def get_id(self) -> uuid.UUID:
        return self.game_id

    def _set_id_(self, game_id):
        if game_id is None:
            self.game_id = uuid.uuid4()
        else:
            self.game_id = game_id
    def get_all_players_ids(self):
        return self.players.keys()

    def set_players(self, players: List[CardPlayer]):
        self.players = {}
        if not players is None:
            for player in players:
                player.set_state_playing()
                self.players[player.player_id] = player

    def set_all_players_playing(self):
        for player in self.players.values():
            player.set_state_playing()

    def has_player(self, player_id):
        return player_id in self.players

    # different games might implement different decks
    def set_card_deck(self, card_deck: CardDeck):
        if card_deck is None:
            self.card_deck = CardDeck(self.get_deck_format())
        else:
            self.card_deck = card_deck

    #the default deck for the game being played (override if a different deck is used)
    def get_deck_format(self) -> DeckFormat:
        return DeckFormat.FIFTY_TWO

    def set_player_order(self, player_order: list):
        if player_order is None:
            self.player_order = []
        else:
            self.player_order = player_order

    #returns first player in queue
    def get_next_player(self):
        return self.players[self.player_order[0]]

    def set_played_cards(self, played_cards: List[PlayedCard]):
        if played_cards is None:
            self.played_cards = []
        else:
            self.played_cards = played_cards

    def add_played_card(self, player_key, card: PlayingCard, game_round: int):
        order = self.number_of_cards_in_round(game_round=game_round)
        self.played_cards.append(PlayedCard(
            player_key=player_key, card=card, game_round=game_round, order=order))

    def get_plays_from_round(self, current_round: int) -> List[PlayedCard]:
        plays_from_round = []
        for played_card in self.played_cards:
            if played_card.round == current_round:
                plays_from_round.insert(played_card.order, played_card)
        return plays_from_round

    def get_plays_from_current_round(self) -> List[PlayedCard]:
        return self.get_plays_from_round(current_round=self.current_round)

    def number_of_cards_in_round(self, game_round: int) -> int:
        if self.current_round < game_round:
            return 0

        plays_count = 0
        for played_card in self.played_cards:
            if played_card.round == game_round:
                plays_count += 1

        return plays_count

    def get_player_cards(self, player_key):
        if not self.players.__contains__(player_key):
            raise Exception("game doens't contain player")
        player = self.players[player_key]

        return player.show_hand()
    
    def get_player_valid_cards(self, player_key):
        player = self.players[player_key]

        if self.is_round_start():
            return player.show_hand()

        valid_cards = []
        for card in player.show_hand():
            if self.is_card_valid(player=player, card=card):
                valid_cards.append(card)
        return valid_cards
    
    def is_round_start(self) -> bool:
        return self.game_state == GameStateEnum.ROUND_START or self.game_state == GameStateEnum.STARTED
    
    def is_players_turn(self, player_id):
        return self.player_order[0] == player_id

    def set_state_round_start(self):
        self.game_state = GameStateEnum.ROUND_START

    def set_state_playing_phase(self):
        self.game_state = GameStateEnum.PLAYING_PHASE
        
    # reusable methods
    def exists_players_playing(self):
        for player in self.players.values():
            if player.is_playing():
                return True
        return False

    def number_of_playing_players(self):
        count = 0
        for player in self.players.values():
            if player.is_playing():
                count += 1
        return count

    def deal_cards(self):
        for player in self.players.keys():
            self.deal_n_cards_to_player(player, self.cards_per_player)

    def rotate_player_order(self):
        self.rotate_player_order_n_times(1)

    def rotate_player_order_n_times(self, n: int):
        if n >= len(self.player_order):
            n = len(self.player_order) % n
        self.player_order = self.player_order[n:] + self.player_order[:n]

    def inverse_rotate_player_order(self):
        self.inverse_rotate_player_order_n_times(1)

    def inverse_rotate_player_order_n_times(self, n):
        size = len(self.player_order)
        if n >= size:
            n = size % n
        rotate = size-n
        self.player_order = self.player_order[rotate:] + \
            self.player_order[:rotate]

    def deal_n_cards_to_player(self, player_key, nCards: int):
        hand = self.card_deck.deal_n_cards(nCards)
        self.players[player_key].deal_cards(hand)
    
    #probably doesnt need to be overriden unless you need to change validations
    def play_card(self, player_key, card):
        player = self.players[player_key]

        self.validate_player(player=player, card=card)
        if self.is_card_valid(player=player, card=card):
            self._play_card(player=player, card=card)
            self._after_play_card_routine()
        else:
            raise Exception("Invalid Card")

    # overridable methods

    # function called by play_card method that executes the routine of playing a card (may change from game to game)
    def _play_card(self, player: CardPlayer, card: PlayingCard):
        player.play_card(card)
        self.add_played_card(player_key=player.player_id,
                             card=card,game_round=self.current_round)
        self.player_state_change_after_play(player)

    #state the player is left in after sucessfully playing a card (default doesnt change player state)
    def player_state_change_after_play(self, player):
        pass

    # routines done after played card has been accepted and transaction has ended
    # default rotates the order of the players and checks for round/game end
    def _after_play_card_routine(self):
        self.rotate_player_order()
        if self.end_round():
            self.end_game()

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

        self.set_state_round_start()
        return True
    
    #checks if round is over
    def can_round_end(self) -> bool:
        if self.exists_players_playing():
            return False
        return True

    # end game called by play_card to execute game ending routine if game is over
    def end_game(self) -> bool:
        if self.is_game_over():
            return True
        
        if self.can_game_end():
            self.game_state = GameStateEnum.GAME_END
            return True
        return False

    def can_game_end(self) -> bool:
        if not self.card_deck.is_empty():
            return False

        for player in self.players.values():
            if player.has_cards():
                return False
        return True

    def validate_player(self, player: CardPlayer, card: PlayingCard):
        if not player.is_playing():
            raise Exception(f'Player {player.player_id} cant play')
        if self.player_order[0] != player.player_id:
            raise Exception(f"It's not {player.player_id}'s turn")
        if not player.has_card(card):
            raise Exception(
                f"Player {player.player_id} doesn't own card {card}")

    def start_game(self):
        self.card_deck.build_deck()
        self.card_deck.shuffle()
        self.deal_cards()
        self.order_players()
        self.game_state = GameStateEnum.STARTED

    def order_players(self):
        if len(self.player_order) != len(self.players):
            player_order = []
            for player in self.players:
                order_size = len(player_order)
                if order_size != 0:
                    for order_index in range(order_size):
                        if order_index == order_size - 1 or self.players[player].team != self.players[player].team:
                            player_order.append(player)
                            break
                else:
                    player_order.append(player)
            self.player_order = player_order

            if self.first_player_id is None:
                self.first_player_id = player_order[0]
            else:
                count = 0
                while self.player_order[0] != self.first_player_id  and count < len(self.player_order):
                    self.rotate_player_order()
                    count += 1

    def get_teams_points_dict(self) -> dict:
        teams = {}
        for player in self.players:
            team = self.players[player].team
            if not team in teams:
                teams[team] = 0
            teams[team] += self.players[player].points
        return teams

    def get_winning_players(self) -> List[CardPlayer]:
        teams = self.get_teams_points_dict()
        winning_team = None
        for team in teams:
            if not winning_team is None:
                if teams[team] > teams[winning_team]:
                    winning_team = team
            else:
                winning_team = team
        winning_players = []
        for player in self.players:
            if self.players[player].team == winning_team:
                winning_players.append(player)
        
    # default validation for player in method play_card method (probably doesnt need to be overriden)
    def is_card_valid(self, player: CardPlayer, card: PlayingCard) -> bool:
        return self.is_card_suit_valid(player=player, card=card) and self.is_card_rank_valid(player=player, card=card)

    # validation of card suit played in method play_card
    def is_card_suit_valid(self, player: CardPlayer, card: PlayingCard) -> bool:
        return True

    # card rank validation called by play_card method
    # default does not validate rank (probably usefull for climbing card games)
    def is_card_rank_valid(self, player: CardPlayer, card: PlayingCard) -> bool:
        return True

    def quit(self, player_key) -> bool:
        raise NotImplementedError(
            "Implement 'quit' in class 'CardGame'")

    def player_pass(self, player):
        raise NotImplementedError(
            "Implement 'player_pass' in class 'CardGame'")

    def bet(self, player, bet):
        raise NotImplementedError(
            "Implement 'bet' in class 'CardGame'")

    def get_round_winner(self, current_round) -> PlayedCard:
        raise NotImplementedError(
            "Implement 'get_round_winner' from class 'card_game'")

    def get_round_points(self, current_round) -> int:
        raise NotImplementedError(
            "Implement 'get_round_points' from class 'card_game'")

    def is_game_over(self) -> bool:
        return self.game_state == GameStateEnum.GAME_END

    def compare_cards(self, card1: PlayingCard, card2: PlayingCard) -> PlayingCard:
        raise NotImplementedError(
            "Implement 'compare_cards' from class 'card_game'")
