import Mechanics


def justDessertsCondition(game, card, target):
    opponent = card.currentOwner.opponent
    if(all(card is None for card in opponent.monsterZone)):
        return False

    return True


def justDesserts(game, card, target):
    opponent = card.currentOwner.opponent
    damageAmount = 0
    for monster in opponent.monsterZone:
        if monster is not None:
            damageAmount += 500

    Mechanics.inflictDamage(opponent, damageAmount)


def reinforcementsCondition(game, card, target):
    field = game.field
    if(all(card is None for card in field.p1MonsterZone) and all(card is None for card in field.p2MonsterZone)):
        return False

    return True


def reinforcements(game, card, target):
    field = game.field
    targets = []
    for monster in field.p1MonsterZone:
        if monster is not None and monster.faceUp is True:
            targets.append(monster)

    for monster in field.p2MonsterZone:
        if monster is not None and monster.faceUp is True:
            targets.append(monster)

    i = 0
    for monster in targets:
        print(f'{i}. {monster.name}')

    value = int(input('Enter target: '))

    while(value < 0 or value > targets.length):
        value = int(input('Enter target: '))

    target = targets[value]

    target.attack += 500

    game.effects.append({
        'card': card,
        'check': 'end of turn',
        'turnActivated': game.turn,
        'end of turn': reinforcementsEndEffect,
        'target': target,
    })


def reinforcementsEndEffect(effectInfo, game):
    monster = effectInfo['target']
    if(monster.location == monster.currentOwner.monsterZone or monster.location == monster.originalOwner.monsterZone):
        monster.attack -= 500


def trapHoleCondition(game, card, target):
    opponent = card.currentOwner.opponent
    if(all(card is None for card in opponent.monsterZone)):
        return False

    if (target.attack < 1000):
        return False

    return True


def trapHole(game, card, target):
    # Mechanics.target(monster)
    Mechanics.destroy(game, target)


def waboku(game, card, target):
    card.currentOwner.effects.append['No battle damage taken']
    card.currentOwner.effects.append['Monsters not destroyed by battle']

    game.effects.append({
        'card': card,
        'check': 'end of turn',
        'turnActivated': game.turn,
        'end of turn': wabokuEndEffect,
        'target': card.currentOwner,
    })


def wabokuEndEffect(effectInfo):
    effectInfo['target'].effects.remove('No battle damage taken')
    effectInfo['target'].effects.remove('Monsters not destroyed by battle')
