import mechanics


def just_desserts_condition(game, card, target):
    opponent = card.current_owner.opponent
    if(all(card is None for card in opponent.monster_zone)):
        return False

    return True


def just_desserts(game, card, target):
    opponent = card.current_owner.opponent
    damage_amount = 0
    for monster in opponent.monster_zone:
        if monster is not None:
            damage_amount += 500

    mechanics.inflict_damage(opponent, damage_amount)


def reinforcements_condition(game, card, target):
    field = game.field
    if(all(card is None for card in field.p1_monster_zone) and all(card is None for card in field.p2_monster_zone)):
        return False

    return True


def reinforcements(game, card, target):
    field = game.field
    targets = []
    for monster in field.p1_monster_zone:
        if monster is not None and monster.face_up is True:
            targets.append(monster)

    for monster in field.p2_monster_zone:
        if monster is not None and monster.face_up is True:
            targets.append(monster)

    i = 0
    for monster in targets:
        print(f'{i}. {monster.name}')

    value = int(input('Enter target: '))

    while(value < 0 or value > len(targets)):
        value = int(input('Enter target: '))

    target = targets[value]

    target.attack += 500

    game.effects.append({
        'card': card,
        'check': 'end of turn',
        'turnActivated': game.turn_counter,
        'end of turn': reinforcements_end_effect,
        'target': target,
    })


def reinforcements_end_effect(effect_info, game):
    monster = effect_info['target']
    if(monster.location == monster.current_owner.monster_zone or monster.location == monster.original_owner.monster_zone):
        monster.attack -= 500

    game.effects.remove(effect_info)


def trap_hole_condition(game, card, target):
    opponent = card.current_owner.opponent
    if(all(card is None for card in opponent.monster_zone)):
        return False

    if (target.attack < 1000):
        return False

    return True


def trap_hole(game, card, target):
    # Mechanics.target(monster)
    mechanics.destroy(game, target)


def waboku(game, card, target):
    card.current_owner.effects.append('No battle damage taken')
    card.current_owner.effects.append('Monsters not destroyed by battle')

    game.effects.append({
        'card': card,
        'check': 'end of turn',
        'turnActivated': game.turn_counter,
        'end of turn': waboku_end_effect,
        'target': card.current_owner,
    })


def waboku_end_effect(effect_info, game):
    effect_info['target'].effects.remove('No battle damage taken')
    effect_info['target'].effects.remove('Monsters not destroyed by battle')
    game.effects.remove(effect_info)
