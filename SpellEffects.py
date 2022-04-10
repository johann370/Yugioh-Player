import Mechanics


def potOfGreed(player):
    Mechanics.draw(player, 2)


def raigekiCondition(opponent):
    if(all(card is None for card in opponent.monsterZone)):
        return False


def raigeki(opponent):
    for monster in opponent.monsterZone:
        Mechanics.destroy(monster)


def darkHoleCondition(field):
    if(all(card is None for card in field.p1MonsterZone) and all(card is None for card in field.p2MonsterZone)):
        return False


def darkHole(field):
    for monster in field.p1MonsterZone:
        Mechanics.destroy(monster)

    for monster in field.p2MonsterZone:
        Mechanics.destroy(monster)


def fissureCondition(opponent):
    # check if there are monsters in opponent's field
    if(all(card is None for card in opponent.monsterZone)):
        return False

    # check if there are face up monsters
    faceUpMonstersInField = False
    for monster in opponent.monsterZone:
        if(monster.faceUp):
            faceUpMonstersInField = True

    return faceUpMonstersInField


def fissure(opponent):
    monsterToDestroy = None
    for monster in opponent.monsterZone:
        if(monsterToDestroy is None):
            monsterToDestroy = monster
        elif(monster.attack < monsterToDestroy.attack):
            monsterToDestroy = monster

    Mechanics.destroy(monsterToDestroy)


def swordsOfRevealingLight(game, opponent, card):
    affectedMonsters = []
    for monster in opponent.monsterZone:
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
