def destroy(card):
    card.currentOwner.monsterZone.remove(card)
    card.owner.graveyard.add(card)


def tribute(cards):
    for card in cards:
        card.currentOwner.monsterZone.remove(card)
        card.owner.graveyard.add(card)


def draw(player, numOfCards):
    player.deck.draw(numOfCards)


def setCard(card, zone):
    card.faceUp = False
    card.currentOwner.STZone[zone] = card
    card.options = ['Activate']


def changeBattlePosition(monster, game):
    if(monster.lastTurnPositionChanged == game.turn or monster.turnSummoned == game.turn):
        return

    if(monster.position == 'attack'):
        monster.position = 'defense'
    elif(monster.position == 'defense'):
        monster.position = 'attack'