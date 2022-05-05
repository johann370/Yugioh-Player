import mechanics


def trap_master_condition(game, card, target):
    if(all(card is None for card in game.p1.st_zone) and all(card is None for card in game.p2.st_zone)):
        return False

    return True


def trap_master(game, card, target):
    owner = card.current_owner
    available_targets = []

    for card in game.p1.st_zone:
        if(card is None):
            continue
        if(card.face_up and card.card_type == 'trap'):
            available_targets.append(card)
        elif(not card.face_up):
            available_targets.append(card)

    for card in game.p2.st_zone:
        if(card is None):
            continue
        if(card.face_up and card.card_type == 'trap'):
            available_targets.append(card)
        elif(not card.face_up):
            available_targets.append(card)

    target = mechanics.choose_card(available_targets, owner)
    # target(target)

    if(not target.face_up):
        mechanics.reveal(target)

    if(target.card_type == 'trap'):
        mechanics.destroy(game, target)


def wall_of_illusion(game, card, target):
    opponent = card.current_owner.opponent
    game.effects.append({
        'card': card,
        'check': 'after damage calculation',
        'after damage calculation': wall_of_illusion_battle,
        'opponent': opponent,
        'end effect': wall_of_illusion_end_effect
    })


def wall_of_illusion_battle(effect_info, game):
    if(effect_info['card'] != game.battle['defender']):
        return

    attacker = game.battle['attacker']
    if(attacker.location is not effect_info['opponent'].monster_zone):
        return

    idx = attacker.location.index(attacker)
    attacker.location[idx] = None
    attacker.owner.hand.cards.append(attacker)
    attacker.location = attacker.owner.hand


def wall_of_illusion_end_effect(effect_info, game):
    game.effects.remove(effect_info)


def man_eater_bug_condition(game, card, target):
    if(all(card is None for card in game.p1.monster_zone) and all(card is None for card in game.p2.monster_zone)):
        return False

    return True


def man_eater_bug(game, card, target):
    owner = card.current_owner
    available_targets = []

    for card in game.p2.monster_zone:
        if(card is None):
            continue
        available_targets.append(card)

    for card in game.p1.monster_zone:
        if(card is None):
            continue
        available_targets.append(card)

    # Mechanics.target(monster)
    monster = mechanics.choose_card(available_targets, owner)
    mechanics.destroy(game, monster)
