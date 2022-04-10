import Mechanics


def justDessertsCondition(opponent):
    if(all(card is None for card in opponent.monsterZone)):
        return False


def justDesserts(opponent):
    damageAmount = 0
    for monster in opponent.monsterZone:
        if monster is not None:
            damageAmount += 500

    Mechanics.inflictDamage(opponent, damageAmount)


def reinforcementsCondition(field):
    if(all(card is None for card in field.p1MonsterZone) and all(card is None for card in field.p2MonsterZone)):
        return False


def reinforcements(game, card):
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

    value = input('Enter target')

    while(value < 0 or value > targets.length):
        value = input('Enter target')

    target = targets[value]

    target.attack += 500

    game.effects.append({
        'card': card,
        'check': 'end of turn',
        'turnActivated': game.turn,
        'end effect': reinforcementsEndEffect,
        'target': target
    })


def reinforcementsEndEffect(effectInfo, game):
    effectInfo['target'].attack -= 500
