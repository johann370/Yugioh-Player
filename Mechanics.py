def destroy(monster, player, field):
    if(player.name == 'p1'):
        field.p1MonsterZone.remove(monster)
    elif(player.name == 'p2'):
        field.p2MonsterZone.remove(monster)

    player.graveyard.add(monster)


def destroy(card, field):
    if(card.currentOwner.name == 'p1'):
        field.p1MonsterZone.remove(card)
    elif(card.currentOwner.name == 'p2'):
        field.p2MonsterZone.remove(card)

    card.owner.graveyard.add(card)
