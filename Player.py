from Banished import Banished
from Deck import Deck
from Graveyard import Graveyard
from Hand import Hand


class Player:
    def __init__(self, name, deck, lp):
        self.name = name
        self.deck = Deck(deck, self)
        self.lp = lp
        self.graveyard = Graveyard()
        self.banished = Banished()
        self.hand = Hand([], 0)
