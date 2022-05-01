class Hand:
    def __init__(self, cards, size):
        self.cards = cards
        self.size = size

    def printHand(self):
        for i in range(len(self.cards)):
            print(f'{i}. {self.cards[i].name}')
