import random


class Deck:
    def __init__(self, cards, player):
        self.cards = cards
        self.player = player
        for card in cards:
            card.setOwner(player)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, numOfCards):
        for i in range(numOfCards):
            if(self.cards):
                card = self.cards.pop(0)
                self.player.hand.cards.append(card)
            else:
                print('Deck is empty')
