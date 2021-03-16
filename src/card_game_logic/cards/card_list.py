import numpy as np
from card_game_logic.cards.card import PlayingCard
from card_game_logic.cards.card_enums import Rank, Suit


class CardList:

    def __init__(self, card_list: [PlayingCard] = None):
        self.set_card_list(card_list)

    def set_card_list(self, new_card_list: [PlayingCard]):
        if new_card_list is None:
            self._card_list = []
        else:
            self._card_list = new_card_list

    def shuffle(self):
        np.random.shuffle(self._card_list)

    def deal_card(self) -> PlayingCard:
        dealt_card = self._card_list[0]
        self._card_list = self._card_list[1:]

        return dealt_card

    def deal_n_cards(self, n) -> [PlayingCard]:
        cards_dealt = self._card_list[0:n]
        self._card_list = self._card_list[n:]
        return cards_dealt

    def add_card(self, card: PlayingCard) -> bool:
        self._card_list.append(card)
        return True

    def remove_card(self, card: PlayingCard) -> bool:
        if(self._card_list.__contains__(card)):
            self._card_list.remove(card)
            return True
        return False

    def contains_card(self, card: PlayingCard) -> bool:
        return self._card_list.__contains__(card)

    def contains_card_of_suit(self, suit: Suit) -> bool:
        for card in self._card_list:
            if card.suit == suit:
                return True
        return False

    def contains_card_of_rank(self, rank: Rank) -> bool:
        for card in self._card_list:
            if card.rank == rank:
                return True
        return False

    def add_cards(self, cards: [PlayingCard]):
        self._card_list = self._card_list + cards

    def list_size(self):
        return len(self._card_list)

    def show_cards(self) -> [PlayingCard]:
        return self._card_list
    # def sort_by_rank(self, sorter):

    def sort_by_rank(self):
        self._card_list.sort(key=lambda x: x.rank)

    def sort_by_suit(self):
        self.sort_by_rank()
        self._card_list.sort(key=lambda x: x.suit)

    def __eq__(self, other):
        if isinstance(other, CardList):
            size = self.list_size()
            for i in range(0, size):
                if not other.show_cards()[i] == self.show_cards()[i]:
                    return False
            return True
        return False

    def similar(self, other):
        if isinstance(other, CardList):
            for card in self._card_list:
                if not other.contains_card(card):
                    return False
            return True
        return False

    def __print_list__(self):
        for card in self._card_list:
            print(card)
