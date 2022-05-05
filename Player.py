from banished import Banished
from deck import Deck
from graveyard import Graveyard
from hand import Hand


class Player:
    def __init__(self, name, deck, lp):
        self.name = name
        self.deck = Deck(deck, self)
        self.lp = lp
        self.graveyard = Graveyard()
        self.banished = Banished()
        self.hand = Hand([], 0)
        self.monsterZone = [None] * 5
        self.STZone = [None] * 5
        self.fieldSpell = None
        self.effects = []
        self.opponent = None
