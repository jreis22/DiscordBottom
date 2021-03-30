
from enum import Enum


class GameStateEnum(Enum):
    CREATED = 0
    DEAL_CARDS = 10
    STARTED = 1
    ROUND_START = 2
    ROUND_END = 3
    BETTING_ROUND = 9
    PLAYING_PHASE = 4
    GAME_END = 5
    CANCELLED = 6
    SURRENDER = 7


class GameState:
    def __init__(self, name: str, state_type: GameStateEnum):
        self.name = name
        self.state_type = state_type

    # ?
    def run(self):
        pass


class GameStateMachine:

    def __init__(self, current_state: GameState, possible_transitions: [GameStateEnum]):
        self.current = current_state
        self.possible_transitions = possible_transitions

    def advance_state(self, next_state: GameState):
        if self.validate_state_change(next_state):
            self.current_state = next_state

    def validate_state_change(self, next_state: GameStateEnum) -> bool:
        raise NotImplementedError(
            "Implement 'player_pass' in class 'CardGame'")
