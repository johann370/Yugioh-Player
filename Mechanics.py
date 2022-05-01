from Chain import Chain
from dataclasses import Field, field
from Card import Card
from Monster import Monster


def destroyByBattle(monster):
    if('Monsters not destroyed by battle' in monster.currentOwner.effects):
        return

    destroy(monster)


def destroy(card):
    if card is None:
        return
    elif(card not in card.currentOwner.monsterZone):
        return

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


def changeBattlePosition(monster, game):
    if(monster.lastTurnPositionChanged == game.turn or monster.turnSummoned == game.turn):
        return

    if(monster.position == 'attack'):
        monster.position = 'defense'
    elif(monster.position == 'defense'):
        monster.position = 'attack'
        if(not monster.faceUp):
            flip(monster)


def inflictDamage(player, amount):
    player.lp -= amount


def activateCard(card, game):
    card.effect.payCost()

    game.chain.addChainLink(card)

    checkForResponse(game)


def flip(monster):
    monster.faceUp = True


def chooseCard(options):
    for i in range(len(options)):
        print(f'{i}. {options[i].name}')

    value = int(input('Choose card: '))

    while(value < 0 and value > len(options)):
        value = int(input('Choose valid card: '))

    return options[value]


def reveal(card):
    print(card.cardName)


def checkForResponse(game, player, responses):
    if(all(card is None for card in player.STZone)):
        return

    availableCards = []

    for card in player.STZone:
        if card is None:
            continue
        if(card.spellSpeed < game.chain.spellSpeed):
            continue
        for response in responses:
            if (response in card.effect.trigger and card not in availableCards):
                availableCards.append(card)

    if (not availableCards):
        return

    availableCards.append(None)

    response = chooseCard(availableCards)

    if (response is None):
        return False

    addToChain(response, game)

    return True


def createChain(game, card):
    if(game.chain):
        return

    addToChain(card, game)
    game.chain.resolve()


def addToChain(card, game):
    card.effect.payCost()

    game.chain.addChainLink(card)

    response = checkForResponse(
        game, card.currentOwner.opponent, card.effect.responses)

    if(not response):
        checkForResponse(game, card.currenOwner, card.effect.responses)


def targetMonster(cards):
    monsterOnField = []

    for i in range(len(Field.p1Monster+Field.p2Monster)):
        monsterOnField.append(i)

    print(f'monsters on field: {monsterOnField}')
    target = int(input('Target Monster'))

    while(target not in monsterOnField):
        print(f'monsters on field: {monsterOnField}')
        target = int(input('Target Monster'))

    return target
