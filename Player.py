from Hand import Hand


class Player:
    def __init__(self, hand, lp):
        self.hand = Hand(hand, len(hand))
        self.lp = lp
