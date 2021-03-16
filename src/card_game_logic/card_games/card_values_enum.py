from enum import Enum
from card_game_logic.cards.card_enums import Rank

#enum
class CardValuesEnum(Enum):

    #ace-ten-games point system
    ACE_TEN = {
        Rank.ACE.value: 11,
        Rank.TEN.value: 10,
        Rank.KING.value: 4,
        Rank.QUEEN.value: 3,
        Rank.JACK.value: 2
    }    #ace-seven (for sueca and bisca like games)
    ACE_SEVEN = {
        Rank.ACE.value: 11,
        Rank.SEVEN.value: 10,
        Rank.KING.value: 4,
        Rank.JACK.value: 3,
        Rank.QUEEN.value: 2
    }

    PRESIDENT = {
        Rank.JOKER.value: 20,
        Rank.TWO.value: 11,
        Rank.ACE.value: 10,
        Rank.KING.value: 4,
        Rank.QUEEN.value: 3,
        Rank.JACK.value: 2
    }

    ROOK = {
        Rank.JOKER.value: 20,
        Rank.ACE.value: 10,
        Rank.TEN.value: 10,
        Rank.FIVE.value: 5,
    }