import numpy as np
import json
from card_game_logic.cards.card_enums import Suit, Rank

class CardImageDictionary:
    _cardImageDict = {}

    @staticmethod
    def set_cardImageDictionary(dictionary):
        CardImageDictionary._cardImageDict = dictionary

    @staticmethod
    def get_card_image(suit: Suit, rank: Rank):
        name = CardImageDictionary._cardImageDict[suit.name][rank.name]["EMOJI_NAME"]
        id = CardImageDictionary._cardImageDict[suit.name][rank.name]["EMOJI_ID"]

        return f"<:{name}:{id}>"

    @staticmethod
    def load_deck(FILE_NAME="cards-config.json"):
            cards_config = json.load(open(FILE_NAME, 'r'))
            ranks = Rank.get_all()
            for suit in Suit.get_all():

                if not suit.name in cards_config:
                    raise KeyError(f"{suit.name} key not present in loaded cards configuration file")
                else:
                    for rank in ranks:

                        if not rank.name in cards_config[suit.name]:
                            raise KeyError(f"{rank.name} key wasn't found in {suit.name} key in the loaded cards configuration file")                        

            CardImageDictionary.set_cardImageDictionary(cards_config)

    @staticmethod
    def random_card():
        rank = np.random.choice(Rank.get_all())
        suit = np.random.choice(Suit.get_all())

        return CardImageDictionary.get_card_image(suit=suit, rank=rank)