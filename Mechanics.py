from chain import Chain
from dataclasses import Field, field

from player import Player


def destroyByBattle(game, monster):
    if('Monsters not destroyed by battle' in monster.currentOwner.effects):
        return

    destroy(game, monster)


def destroy(game, card):
    if card is None:
        return
    elif(card not in card.currentOwner.monsterZone and card not in card.currentOwner.STZone):
        return

    idx = card.location.index(card)
    card.location[idx] = None
    card.owner.graveyard.cards.append(card)
    card.location = card.owner.graveyard.cards

    for effect in game.effects:
        if(effect['card'] == card and 'end effect' in effect):
            effect['end effect'](effect, game)


def tribute(cards):
    for card in cards:
        card.currentOwner.monsterZone.remove(card)
        card.owner.graveyard.add(card)


def draw(player, numOfCards):
    return player.deck.draw(numOfCards)


def setCard(card):
    zone = chooseZone(card.currentOwner.STZone)
    card.faceUp = False
    card.currentOwner.hand.cards.remove(card)
    card.currentOwner.STZone[zone] = card
    card.location = card.currentOwner.STZone


def changeBattlePosition(monster, game):
    if(monster.lastTurnPositionChanged == game.turnCounter or monster.turnSummoned == game.turnCounter):
        return

    if(monster.position == 'attack'):
        monster.position = 'defense'
    elif(monster.position == 'defense'):
        monster.position = 'attack'
        if(not monster.faceUp):
            flip(monster)
    monster.lastTurnPositionChanged = game.turnCounter


def inflictBattleDamage(player, damageAmount):
    if('No battle damage taken' in player.effects):
        return

    inflictDamage(player, damageAmount)


def inflictDamage(player, amount):
    player.lp -= amount


def activateCard(game, card):
    if(game.chain is None):
        createChain(game, card)


def flip(game, monster):
    monster.faceUp = True
    if('Flip' in monster.monsterType):
        createChain(game, monster, None)


def chooseCard(options, player):
    for i in range(len(options)):
        if(options[i] is not None):
            if(isinstance(options[i], Player)):
                print(f'{i}. {options[i].name}')
            elif(options[i].faceUp is None or options[i].faceUp or options[i].currentOwner == player):
                print(
                    f'{i}. {options[i].name} ({options[i].currentOwner.name})')
            elif(not options[i].faceUp):
                print(f'{i}. Face Down ({options[i].currentOwner.name})')
        elif(options[i] is None):
            print(f'{i}. Cancel')

    value = int(input('Choose card: '))

    while(value < 0 and value > len(options)):
        value = int(input('Choose valid card: '))

    return options[value]


def reveal(card):
    print(card.name)


def checkForResponse(game, player, responses, previousCard):
    if(all(card is None for card in player.STZone)):
        return False

    availableCards = []

    for card in player.STZone:
        if card is None:
            continue
        if(game.chain is not None and card.spellSpeed < game.chain.spellSpeed):
            continue
        if(card == previousCard):
            continue
        if(game.chain is not None and card in game.chain.cards):
            continue
        for response in responses:
            if(card.effect.trigger is None) or response not in card.effect.trigger:
                continue
            elif (card.effect.condition is None or card.effect.condition(game, card, previousCard) and card not in availableCards):
                availableCards.append(card)

    if (not availableCards):
        return False

    availableCards.append(None)

    response = chooseCard(availableCards, player)

    if (response is None):
        return False

    if(game.chain is None):
        createChain(game, response, previousCard)
    else:
        addToChain(game, response, previousCard)

    return True


def createChain(game, card, previousCard):
    if(game.chain and not game.chain.cards):
        return

    game.chain = Chain()
    addToChain(game, card, previousCard)
    game.chain.resolve(game)
    game.chain = None


def addToChain(game, card, previousCard):
    card.effect.payCost()
    game.chain.addChainLink(card, previousCard)

    response = checkForResponse(
        game, card.currentOwner.opponent, card.effect.responses, card)

    if(not response):
        checkForResponse(game, card.currentOwner, card.effect.responses, card)


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


def chooseZone(zone):
    availableZones = []

    for i in range(len(zone)):
        if(zone[i] is None):
            availableZones.append(i)

    print(f'Available zones: {availableZones}')
    zoneNum = int(input('Choose a zone: '))

    while(zoneNum not in availableZones):
        print(f'Available zones: {availableZones}')
        zoneNum = int(input('Invalid zone, please choose a zone: '))

    return zoneNum


def sendToGrave(cards):
    if(not cards):
        return

    for card in cards:
        idx = card.location.index(card)
        card.location[idx] = None
        card.owner.graveyard.cards.append(card)
        card.location = card.owner.graveyard.cards


def prompt(player, cards):
    card = chooseCard(cards, player)

    return card
