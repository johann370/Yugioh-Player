import Mechanics
import Summon


def potOfGreed(game, card, target):
    Mechanics.draw(card.currentOwner, 2)


def raigekiCondition(game, card, target):
    opponent = card.currentOwner.opponent
    if(all(card is None for card in opponent.monsterZone)):
        return False

    return True


def raigeki(game, card, target):
    opponent = card.currentOwner.opponent
    for monster in opponent.monsterZone:
        if(monster is None):
            continue
        Mechanics.destroy(game, monster)


def darkHoleCondition(game, card, target):
    field = game.field
    if(all(card is None for card in field.p1MonsterZone) and all(card is None for card in field.p2MonsterZone)):
        return False

    return True


def darkHole(game, card, target):
    field = game.field
    for monster in field.p1MonsterZone:
        if(monster is None):
            continue
        Mechanics.destroy(game, monster)

    for monster in field.p2MonsterZone:
        if(monster is None):
            continue
        Mechanics.destroy(game, monster)


def fissureCondition(game, card, target):
    opponent = card.currentOwner.opponent
    # check if there are monsters in opponent's field
    if(all(card is None for card in opponent.monsterZone)):
        return False

    # check if there are face up monsters
    faceUpMonstersInField = False
    for monster in opponent.monsterZone:
        if(monster is None):
            continue
        if(monster.faceUp):
            faceUpMonstersInField = True

    return faceUpMonstersInField


def fissure(game, card, target):
    opponent = card.currentOwner.opponent
    monsterToDestroy = None
    for monster in opponent.monsterZone:
        if(monster is None):
            continue
        if(monsterToDestroy is None):
            monsterToDestroy = monster
        elif(monster.attack < monsterToDestroy.attack):
            monsterToDestroy = monster

    Mechanics.destroy(game, monsterToDestroy)


def swordsOfRevealingLight(game, card, target):
    opponent = card.currentOwner.opponent
    affectedMonsters = []
    for monster in opponent.monsterZone:
        if(monster is None):
            continue
        if(not monster.faceUp):
            Mechanics.flip(game, monster)

        if(monster.canDeclareAttack):
            monster.canDeclareAttack = False
            affectedMonsters.append(monster)

    game.effects.append({
        'card': card,
        'check': 'end phase',
        'turnActivated': game.turnCounter,
        'opponent': opponent,
        'continuousEffect': swordsOfRevealingLightContinuous,
        'end phase': swordsOfRevealingLightEndTurn,
        'counter': 0,
        'affectedMonsters': affectedMonsters,
        'end effect': swordsOfRevealingLightEndEffect
    })


def swordsOfRevealingLightContinuous(effectInfo, game):
    opponent = effectInfo['opponent']
    for monster in opponent.monsterZone:
        if (monster is None):
            continue
        if(monster.canDeclareAttack):
            monster.canDeclareAttack = False
            effectInfo['affectedMonsters'].append(monster)


def swordsOfRevealingLightEndTurn(effectInfo, game):
    if(game.turnPlayer == effectInfo['opponent']):
        effectInfo['counter'] = effectInfo['counter'] + 1

    if(effectInfo['counter'] == 3):
        swordsOfRevealingLightEndEffect(effectInfo, game)


def swordsOfRevealingLightEndEffect(effectInfo, game):
    for monster in effectInfo['affectedMonsters']:
        monster.canDeclareAttack = True
    Mechanics.destroy(game, effectInfo['card'])
    game.effects.remove(effectInfo)


def monsterRebornCondition(game, card, target):
    if(not game.p1.graveyard.cards and not game.p2.graveyard.cards):
        return False

    monstersInGrave = False

    for card in game.p1.graveyard.cards:
        if card.cardType == 'Monster':
            monstersInGrave = True

    for card in game.p2.graveyard.cards:
        if card.cardType == 'Monster':
            monstersInGrave = True

    return monstersInGrave


def monsterReborn(game, card, target):
    owner = card.currentOwner
    availableTargets = []

    for card in game.p1.graveyard:
        if card.cardType == 'Monster':
            availableTargets.append(card)

    for card in game.p2.graveyard:
        if card.cardType == 'Monster':
            availableTargets.append(card)

    monster = Mechanics.chooseCard(availableTargets, owner)
    # target(monster)

    monster.currentOwner = owner
    Summon.summon('special', monster, game)


def deSpellCondition(game, card, target):
    if(all(card is None for card in game.field.p1STZone) and all(card is None for card in game.field.p2STZone)):
        return False

    return True


def deSpell(game, card, target):
    owner = card.currentOwner
    availableTargets = []

    for card in game.p1.STZone:
        if(card is None):
            continue
        if(card.faceUp and card.cardType == 'spell'):
            availableTargets.append(card)
        elif(not card.faceUp):
            availableTargets.append(card)

    for card in game.p2.STZone:
        if(card is None):
            continue
        if(card.faceUp and card.cardType == 'spell'):
            availableTargets.append(card)
        elif(not card.faceUp):
            availableTargets.append(card)

    target = Mechanics.chooseCard(availableTargets, owner)
    # target(target)

    if(not target.faceUp):
        Mechanics.reveal(target)

    if(target.cardType == 'spell'):
        Mechanics.destroy(game, target)


def changeOfHeartCondition(game, card, target):
    opponent = card.currentOwner.opponent
    if(all(card is None for card in opponent.monsterZone)):
        return False

    return True


def changeOfHeart(game, card, target):
    opponent = card.currentOwner.opponent
    availableTargets = []
    for monster in opponent.monsterZone:
        if monster is not None:
            availableTargets.append(monster)

    target = Mechanics.chooseCard(availableTargets, card.currentOwner)
    # target(target)

    idx = target.location.index(target)
    target.location[idx] = None

    zone = Summon.chooseZone(card.currentOwner)
    card.currentOwner.monsterZone[zone] = target
    target.location = card.currentOwner.monsterZone

    game.effects.append({
        'card': card,
        'check': 'end phase',
        'turnActivated': game.turnCounter,
        'end phase': changeOfHeartEndEffect,
        'target': target,
        'target player': opponent,
        'location': target.location,
        'original location': opponent.monsterZone,
    })


def changeOfHeartEndEffect(effectInfo, game):
    target = effectInfo['target']
    if(game.turnCounter is not effectInfo['turnActivated']):
        return

    if(target.location is not effectInfo['location']):
        return

    zone = Summon.chooseZone(effectInfo['target player'])

    idx = target.location.index(target)
    target.location[idx] = None

    effectInfo['original location'][zone] = target
    target.location = effectInfo['original location']
    game.effects.remove(effectInfo)
