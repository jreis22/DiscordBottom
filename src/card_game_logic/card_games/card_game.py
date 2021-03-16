import uuid
from card_game_logic.player import CardPlayer
from card_game_logic.cards.card_deck import CardDeck
from card_game_logic.cards.card_enums import DeckFormat
from card_game_logic.card_games.game_state import GameStateEnum
from card_game_logic.cards.card import PlayingCard
from card_game_logic.card_games.played_card import PlayedCard


class CardGame():

    # rounds are
    def __init__(self, cards_per_player: int, current_round: int = 1, game_id: uuid.UUID = None, players: [] = None,
                 card_deck: CardDeck = None,
                 game_state: GameStateEnum = GameStateEnum.CREATED,
                 player_order: [] = None, played_cards: [] = None):
        self.set_players(players)
        self.set_card_deck(card_deck)
        self.game_state = game_state
        self.cards_per_player = cards_per_player
        self.set_player_order(player_order)
        self.set_played_cards(played_cards)
        self._set_id_(game_id)
        self.current_round = current_round

    # setters & getters
    
    def _set_id_(self, game_id):
        if game_id is None:
            self.game_id = uuid.uuid1()
        else:
            self.game_id = game_id

    def get_id(self) -> uuid.UUID:
        return self.game_id

    def set_players(self, players: []):
        self.players = {}
        if not players is None:
            for player in players:
                self.players[player.player_id] = player

    def set_all_players_playing(self):
        for player in self.players.values():
            player.set_state_playing()

    # different games might implement different decks
    def set_card_deck(self, card_deck: CardDeck):
        if card_deck is None:
            self.card_deck = CardDeck(self.get_deck_format())
        else:
            self.card_deck = card_deck

    #the default deck for the game being played (override if a different deck is used)
    def get_deck_format(self) -> DeckFormat:
        return DeckFormat.FIFTY_TWO

    def set_player_order(self, player_order: []):
        if player_order is None:
            self.player_order = []
        else:
            self.player_order = player_order

    def set_played_cards(self, played_cards: []):
        if played_cards is None:
            self.played_cards = []
        else:
            self.played_cards = played_cards

    def add_played_card(self, player_key, card: PlayingCard, round: int):
        self.played_cards.append(PlayedCard(
            player_key=player_key, card=card, round=round))

    def get_plays_from_round(self, current_round: int):
        if self.current_round < current_round:
            raise Exception(f"Round wasn't reached yet")
        
        plays_from_round = []
        for played_card in self.played_cards:
            if played_card.round == current_round:
                plays_from_round.append(played_card)

        return plays_from_round

    def get_player_cards(self, player_key):
        if not self.players.__contains__(player_key):
            raise Exception("game doens't contain player")
        player = self.players[player_key]

        return player.show_hand()

    # reusable methods
    def exists_players_playing(self):
        for player in self.players.values():
            if player.is_playing():
                return True
        return False

    def number_of_playing_players(self):
        count = 0
        for player in self.players.keys():
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

    def player_exists(self, player_key) -> bool:
        return player_key in self.players

    # overridable methods
    def start_game(self):
        self.card_deck.build_deck()
        self.card_deck.shuffle()
        self.deal_cards()
        self.game_state = GameStateEnum.STARTED

    def play_card(self, player_key, card):
        raise NotImplementedError(
            "Implement 'play_card' in class 'CardGame'")

    def quit(self, player_key) -> bool:
        raise NotImplementedError(
            "Implement 'quit' in class 'CardGame'")

    def player_pass(self, player):
        raise NotImplementedError(
            "Implement 'player_pass' in class 'CardGame'")

    def bet(self, player, bet):
        raise NotImplementedError(
            "Implement 'bet' in class 'CardGame'")

    def is_round_over(self) -> bool:
        raise NotImplementedError(
            "Implement 'is_round_over' from class 'CardGame'")

    def is_game_over(self) -> bool:
        return self.game_state == GameStateEnum.GAME_END

    def compare_cards(self, card1: PlayingCard, card2: PlayingCard) -> PlayingCard:
        raise NotImplementedError(
            "Implement 'compare_cards' from class 'card_game'")
