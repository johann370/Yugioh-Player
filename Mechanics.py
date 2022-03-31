def destroy(card, field):
    if(card.currentOwner.name == 'p1'):
        field.p1MonsterZone.remove(card)
    elif(card.currentOwner.name == 'p2'):
        field.p2MonsterZone.remove(card)

    card.owner.graveyard.add(card)


def tribute(cards, field):
    for card in cards:
        if(card.currentOwner.name == 'p1'):
            field.p1MonsterZone.remove(card)
        elif(card.currentOwner.name == 'p2'):
            field.p2MonsterZone.remove(card)

        card.owner.graveyard.add(card)
