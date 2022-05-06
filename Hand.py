class Hand:
    def __init__(self, cards, size):
        self.cards = cards
        self.size = size

    def print_hand(self):
        for idx, card in enumerate(self.cards):
            print(f'{idx}. {card.name}')
