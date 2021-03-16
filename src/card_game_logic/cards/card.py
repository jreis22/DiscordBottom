from card_game_logic.cards.card_enums import Suit, Rank

class PlayingCard(object):
    def __init__(self, suit: Suit, rank: Rank):
        self.suit = suit
        self.rank = rank
        
    def same_suit(self, other_card):
        if isinstance(other_card, PlayingCard):
            return other_card.suit == self.suit
        return False

    def is_greater(self, other_card, comparator):
        if isinstance(other_card, PlayingCard):
            return comparator(self, other_card)
        return False

    def __eq__(self, other_card):
        if isinstance(other_card, PlayingCard):
            return self.suit == other_card.suit and self.rank == other_card.rank
        return False
    
    def __str__(self):
        return self.rank.name + ' of ' + self.suit.name
        
#card1 = PlayingCard(suit=Suit.HEARTS, rank=Rank.ACE)
#print(card1)
# card2 = PlayingCard(suit=Suit.HEARTS, rank=Rank.KING)