import random


class Deck:
    def __init__(self, cards, player):
        self.cards = cards
        self.player = player
        for card in cards:
            card.set_owner(player)
            card.location = self

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, num_of_cards):
        for i in range(num_of_cards):
            if(self.cards):
                card = self.cards.pop(0)
                card.location = card.current_owner.hand.cards
                self.player.hand.cards.append(card)
            else:
                print('Deck is empty')
                return None

        return True
