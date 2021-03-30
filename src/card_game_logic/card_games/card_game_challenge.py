import uuid
from typing import List, Dict
from card_game_logic.player import CardPlayer
from card_game_logic.card_games.card_game import CardGame
from card_game_logic.card_games.card_game_type import CardGameType
from card_game_logic.card_games.card_game_factory import CardGameFactory

class CardGameChallenge:

    PENDING = 1
    ACCEPTED = 2
    CANCELLED = 0

    def __init__(self, challenger_id, players_list: List[CardPlayer], game_type: CardGameType, challenge_id=None, state=None):
        self.set_players(players_list=players_list)
        self._set_id(challenge_id)
        self._set_state(state)
        self.game_type = game_type
        self.challenger_id = challenger_id

    def set_players(self, players_list: List[CardPlayer]):
        self.players = {}
        if not players_list == []:
            for player in players_list:
                self.players[player.player_id] = player

    def _set_id(self, new_id):
        if not new_id is None:
            self.id = new_id
        else:
            self.id = uuid.uuid4()

    def _set_state(self, state):
        if not state is None:
            self.state = state
        else:
            self.state = CardGameChallenge.PENDING

    def get_id(self):
        return self.id

    def accept(self):
        self._set_state(CardGameChallenge.ACCEPTED)

    def is_cancelled(self) -> bool:
        return self.state == CardGameChallenge.CANCELLED

    def is_accepted(self) -> bool:
        return self.state == CardGameChallenge.ACCEPTED

    def has_player(self, player_id):
        return player_id in self.players

    def quit_challenge(self, player_id):
        player = self.players[player_id]
        player.quit()

        self._set_state(CardGameChallenge.CANCELLED)

    def accept_challenge(self, player_id):
        if self.is_cancelled():
            return
        player = self.players[player_id]
        player.set_state_playing()

        for p in self.players:
            if self.players[p].is_pending():
                return

        self.accept()

    def create_card_game(self) -> CardGame:
        if self.is_accepted():
            factory = CardGameFactory()
            players = list(self.players.values())
            game = factory.create(game_type=self.game_type, players=players)
            game.order_players()
            count = 0
            while game.get_first_player().player_id != self.challenger_id and count <= len(players):
                game.rotate_player_order()
                count += 1
            game.start_game()
            return game
        else:
            raise ValueError("Challenge isn't in accepted state, game cannot be created")


    def __str__(self) -> str:
        message = f"{self.id} ({self.game_type.name}): "
        for player in self.players:
            message += f"{player} "
        return message
        