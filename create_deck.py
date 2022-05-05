from card_database import getCard


def createDeck(deckList):
    with open(deckList) as f:
        lines = f.readlines()

    cards = []

    for line in lines:
        x = line.rstrip('\n').split('x ')

        for i in range(int(x[0])):
            cards.append(getCard(x[1]))

    return cards
