import Mechanics


def trapMasterCondition(game, card, target):
    if(all(card is None for card in game.p1.STZone) and all(card is None for card in game.p2.STZone)):
        return False

    return True


def trapMaster(game, card, target):
    owner = card.currentOwner
    availableTargets = []

    for card in game.p1.STZone:
        if(card is None):
            continue
        if(card.faceUp and card.cardType == 'trap'):
            availableTargets.append(card)
        elif(not card.faceUp):
            availableTargets.append(card)

    for card in game.p2.STZone:
        if(card is None):
            continue
        if(card.faceUp and card.cardType == 'trap'):
            availableTargets.append(card)
        elif(not card.faceUp):
            availableTargets.append(card)

    target = Mechanics.chooseCard(availableTargets, owner)
    # target(target)

    if(not target.faceUp):
        Mechanics.reveal(target)

    if(target.cardType == 'trap'):
        Mechanics.destroy(game, target)


def wallOfIllusion(game, card, target):
    opponent = card.currentOwner.opponent
    game.effects.append({
        'card': card,
        'check': 'after damage calculation',
        'after damage calculation': wallOfIllusionBattle,
        'opponent': opponent,
        'end effect': wallOfIllusionEndEffect
    })


def wallOfIllusionBattle(effectInfo, game):
    if(effectInfo['card'] != game.battle['defender']):
        return

    attacker = game.battle['attacker']
    if(attacker.location is not effectInfo['opponent'].monsterZone):
        return

    idx = attacker.location.index(attacker)
    attacker.location[idx] = None
    attacker.owner.hand.cards.append(attacker)
    attacker.location = attacker.owner.hand


def wallOfIllusionEndEffect(effectInfo, game):
    game.effects.remove(effectInfo)


def manEaterBugCondition(game, card, target):
    if(all(card is None for card in game.p1.monsterZone) and all(card is None for card in game.p2.monsterZone)):
        return False

    return True


def manEaterBug(game, card, target):
    owner = card.currentOwner
    availableTargets = []
    emptyZone = []

    for card in game.p2.monsterZone:
        if(card is None):
            continue
        availableTargets.append(card)

    for card in game.p1.monsterZone:
        if(card is None):
            continue
        availableTargets.append(card)

    # Mechanics.target(monster)
    monster = Mechanics.chooseCard(availableTargets, owner)
    Mechanics.destroy(game, monster)
