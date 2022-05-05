from card_database import get_card


def create_deck(deck_list):
    with open(deck_list) as f:
        lines = f.readlines()

    cards = []

    for line in lines:
        x = line.rstrip('\n').split('x ')

        for i in range(int(x[0])):
            cards.append(get_card(x[1]))

    return cards
