from aenum import Enum, NoAlias

#each card game type specifies the number of players, (0 if its unlimited for now)
class CardGameType(Enum):
    _settings_ = NoAlias
    BISCA = 2
    SUECA = 4
