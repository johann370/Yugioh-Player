import Mechanics
import Summon


def potOfGreed(player):
    Mechanics.draw(player, 2)


def raigekiCondition(opponent):
    if(all(card is None for card in opponent.monsterZone)):
        return False


def raigeki(opponent):
    for monster in opponent.monsterZone:
        if(monster is None):
            continue
        Mechanics.destroy(monster)


def darkHoleCondition(field):
    if(all(card is None for card in field.p1MonsterZone) and all(card is None for card in field.p2MonsterZone)):
        return False


def darkHole(field):
    for monster in field.p1MonsterZone:
        if(monster is None):
            continue
        Mechanics.destroy(monster)

    for monster in field.p2MonsterZone:
        if(monster is None):
            continue
        Mechanics.destroy(monster)


def fissureCondition(opponent):
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


def fissure(opponent):
    monsterToDestroy = None
    for monster in opponent.monsterZone:
        if(monster is None):
            continue
        if(monsterToDestroy is None):
            monsterToDestroy = monster
        elif(monster.attack < monsterToDestroy.attack):
            monsterToDestroy = monster

    Mechanics.destroy(monsterToDestroy)


def swordsOfRevealingLight(game, opponent, card):
    affectedMonsters = []
    for monster in opponent.monsterZone:
        if(monster is None):
            continue
        if(not monster.faceUp):
            Mechanics.flip(monster)

        if(monster.canDeclareAttack):
            monster.canDeclareAttack = False
            affectedMonsters.append(monster)

    game.effects.append({
        'card': card,
        'check': 'end phase',
        'turnActivated': game.turn,
        'opponent': opponent,
        'continuousEffect': swordsOfRevealingLightContinuous,
        'counter': 0,
        'affectedMonsters': affectedMonsters
    })


def swordsOfRevealingLightContinuous(effectInfo):
    opponent = effectInfo['opponent']
    for monster in opponent.monsterZone():
        if(monster.canDeclareAttack):
            monster.canDeclareAttack = False
            effectInfo['affectedMonsters'].append(monster)


def swordsOfRevealingLightEndTurn(effectInfo, game):
    if(effectInfo['counter'] == 3):
        swordsOfRevealingLightEndEffect(effectInfo)

    if(game.turnPlayer == effectInfo['opponent']):
        effectInfo['counter'] += 1


def swordsOfRevealingLightEndEffect(effectInfo):
    for monster in effectInfo['affectedMonsters']:
        monster.canDeclareAttack = True
    Mechanics.destroy(effectInfo['card'])


def monsterRebornCondition(game):
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


def monsterReborn(game, card):
    availableTargets = []

    for card in game.p1.graveyard:
        if card.cardType == 'Monster':
            availableTargets.append(card)

    for card in game.p2.graveyard:
        if card.cardType == 'Monster':
            availableTargets.append(card)

    monster = Mechanics.chooseCard(availableTargets)
    # target(monster)

    monster.currentOwner = card.currentOwner
    Summon.summon('special', monster, game)


def deSpellCondition(game):
    if(all(card is None for card in game.field.p1MonsterZone) and all(card is None for card in game.field.p2MonsterZone)):
        return False


def deSpell(game):
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

    target = Mechanics.chooseCard(availableTargets)
    # target(target)

    if(not target.faceUp):
        Mechanics.reveal(target)

    if(target.cardType == 'spell'):
        Mechanics.destroy(target)


def changeOfHeartCondition(opponent):
    if(all(card is None for card in opponent.monsterZone)):
        return False


def changeOfHeart(game, opponent, card):
    availableTargets = []
    for monster in opponent.monsterZone:
        if monster is not None:
            availableTargets.append(monster)

    target = Mechanics.chooseCard(availableTargets)
    # target(target)

    zone = Summon.chooseZone(card.currentOwner)
    card.currentOwner.monsterZone[zone] = target
    card.location = card.currentOwner.monsterZone

    game.effects.append({
        'card': card,
        'check': 'end phase',
        'turnActivated': game.turn,
        'end effect': changeOfHeartEndEffect,
        'target': target,
        'target player': opponent,
        'location': card.location,
        'original location': opponent.monsterZone
    })


def changeOfHeartEndEffect(effectInfo, game):
    target = effectInfo['target']
    if(game.turn is not effectInfo['turnActivated']):
        return

    if(target.location is not effectInfo['location']):
        return

    zone = Summon.chooseZone(effectInfo['target player'])
    effectInfo['location'].remove(target)
    effectInfo['original location'][zone] = target
    target.location = effectInfo['original location']
