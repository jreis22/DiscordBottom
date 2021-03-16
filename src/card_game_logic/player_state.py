from enum import Enum


class PlayerStateEnum(Enum):
    QUIT = 0
    PLAYING = 1
    PASS = 2
    WON = 3
    LOST = 4