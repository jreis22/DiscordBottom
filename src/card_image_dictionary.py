import numpy as np
from discord import PartialEmoji
import json
from card_game_logic.cards.card_enums import Suit, Rank
from card_game_logic.cards.card import PlayingCard

class CardImageDictionary:
    _cardImageDict = {}
    _cards_ids = {}
    @staticmethod
    def set_cardImageDictionary(dictionary):
        CardImageDictionary._cardImageDict = dictionary

    @staticmethod
    def get_card_emoji(suit: Suit, rank: Rank):
        name = CardImageDictionary._cardImageDict[suit.name][rank.name]["EMOJI_NAME"]
        id = CardImageDictionary._cardImageDict[suit.name][rank.name]["EMOJI_ID"]

        return f"<:{name}:{id}>"

    @staticmethod
    def get_card_by_id(id) -> PlayingCard:
        rank = Rank[CardImageDictionary._cards_ids[str(id)]["RANK"].upper()]
        suit = Suit[CardImageDictionary._cards_ids[str(id)]["SUIT"].upper()]
        return PlayingCard(suit=suit, rank=rank)

    @staticmethod
    def get_suit_emoji(suit: Suit) -> str:
        return CardImageDictionary._cardImageDict[suit.name]["EMOJI"]

    @staticmethod
    def get_card_image_url(suit: Suit, rank: Rank):
        id = CardImageDictionary._cardImageDict[suit.name][rank.name]["EMOJI_ID"]

        return f"https://cdn.discordapp.com/emojis/{id}.png?v=1"

    @staticmethod
    def load_deck(FILE_NAME="cards-config.json"):
        cards_config = json.load(open(FILE_NAME, 'r'))
        ranks = Rank.get_all()
        aux_dict = {}
        for suit in Suit.get_all():

            if not suit.name in cards_config:
                raise KeyError(f"{suit.name} key not present in loaded cards configuration file")
            else:
                for rank in ranks:

                    if not rank.name in cards_config[suit.name]:
                        raise KeyError(f"{rank.name} key wasn't found in {suit.name} key in the loaded cards configuration file")
                    else:
                        emoji_id = cards_config[suit.name][rank.name]["EMOJI_ID"]
                        aux_dict[emoji_id] = { "RANK" : rank.name, "SUIT" : suit.name }

        CardImageDictionary._cards_ids = aux_dict
        CardImageDictionary.set_cardImageDictionary(cards_config)

    @staticmethod
    def is_card_emoji(emoji: PartialEmoji) -> bool:
        if emoji.id is None:
            return False
        return str(emoji.id) in CardImageDictionary._cards_ids