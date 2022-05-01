import Mechanics


def trapMasterCondition(game):
    if(all(card is None for card in game.p1.STZone) and all(card is None for card in game.p2.STZone)):
        return False

    return True


def trapMaster(game):
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

    target = Mechanics.chooseCard(availableTargets)
    # target(target)

    if(not target.faceUp):
        Mechanics.reveal(target)

    if(target.cardType == 'trap'):
        Mechanics.destroy(target)


def wallOfIllusion(game, card, opponent):
    game.effects.append({
        'card': card,
        'check': 'after damage calculation',
        'continuousEffect': wallOfIllusionContinuous,
        'opponent': opponent
    })


def wallOfIllusionContinuous(effectInfo, game):
    attacker = game.battle['attacker']
    if(attacker.location is not effectInfo['opponent'].monsterZone):
        return

    attacker.currentOwner.monsterZone.remove(attacker)
    attacker.owner.hand.cards.append(attacker)
    attacker.location = attacker.owner.hand
