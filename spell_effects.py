import mechanics
import summon


def pot_of_greed(game, card, target):
    mechanics.draw(card.current_owner, 2)


def raigeki_condition(game, card, target):
    opponent = card.current_owner.opponent
    if(all(card is None for card in opponent.monster_zone)):
        return False

    return True


def raigeki(game, card, target):
    opponent = card.current_owner.opponent
    for monster in opponent.monster_zone:
        if(monster is None):
            continue
        mechanics.destroy(game, monster)


def dark_hole_condition(game, card, target):
    field = game.field
    if(all(card is None for card in field.p1_monster_zone) and all(card is None for card in field.p2_monster_zone)):
        return False

    return True


def dark_hole(game, card, target):
    field = game.field
    for monster in field.p1_monster_zone:
        if(monster is None):
            continue
        mechanics.destroy(game, monster)

    for monster in field.p2_monster_zone:
        if(monster is None):
            continue
        mechanics.destroy(game, monster)


def fissure_condition(game, card, target):
    opponent = card.current_owner.opponent
    # check if there are monsters in opponent's field
    if(all(card is None for card in opponent.monster_zone)):
        return False

    # check if there are face up monsters
    face_up_monsters_in_field = False
    for monster in opponent.monster_zone:
        if(monster is None):
            continue
        if(monster.face_up):
            face_up_monsters_in_field = True

    return face_up_monsters_in_field


def fissure(game, card, target):
    opponent = card.current_owner.opponent
    monster_to_destroy = None
    for monster in opponent.monster_zone:
        if(monster is None):
            continue
        if(monster_to_destroy is None):
            monster_to_destroy = monster
        elif(monster.attack < monster_to_destroy.attack):
            monster_to_destroy = monster

    mechanics.destroy(game, monster_to_destroy)


def swords_of_revealing_light(game, card, target):
    opponent = card.current_owner.opponent
    affected_monsters = []
    for monster in opponent.monster_zone:
        if(monster is None):
            continue
        if(not monster.face_up):
            mechanics.flip(game, monster)
        if(monster.can_declare_attack):
            monster.can_declare_attack = False
            affected_monsters.append(monster)

    game.effects.append({
        'card': card,
        'check': 'end phase',
        'turnActivated': game.turn_counter,
        'opponent': opponent,
        'continuous effect': swords_of_revealing_light_continuous,
        'end phase': swords_of_revealing_light_end_turn,
        'counter': 0,
        'affectedMonsters': affected_monsters,
        'end effect': swords_of_revealing_light_end_effect
    })


def swords_of_revealing_light_continuous(effect_info, game):
    opponent = effect_info['opponent']
    for monster in opponent.monster_zone:
        if (monster is None):
            continue
        if(monster.can_declare_attack):
            monster.can_declare_attack = False
            effect_info['affectedMonsters'].append(monster)


def swords_of_revealing_light_end_turn(effect_info, game):
    if(game.turn_player == effect_info['opponent']):
        effect_info['counter'] = effect_info['counter'] + 1

    if(effect_info['counter'] == 3):
        swords_of_revealing_light_end_effect(effect_info, game)


def swords_of_revealing_light_end_effect(effect_info, game):
    for monster in effect_info['affectedMonsters']:
        monster.can_declare_attack = True
    mechanics.destroy(game, effect_info['card'])
    game.effects.remove(effect_info)


def monster_reborn_condition(game, card, target):
    if(not game.p1.graveyard.cards and not game.p2.graveyard.cards):
        return False

    monsters_in_grave = False

    for card in game.p1.graveyard.cards:
        if card.card_type == 'Monster':
            monsters_in_grave = True

    for card in game.p2.graveyard.cards:
        if card.card_type == 'Monster':
            monsters_in_grave = True

    return monsters_in_grave


def monster_reborn(game, card, target):
    owner = card.current_owner
    available_targets = []

    for card in game.p1.graveyard:
        if card.card_type == 'Monster':
            available_targets.append(card)

    for card in game.p2.graveyard:
        if card.card_type == 'Monster':
            available_targets.append(card)

    monster = mechanics.choose_card(available_targets, owner)
    # target(monster)

    monster.current_owner = owner
    summon.summon('special', monster, game)


def de_spell_condition(game, card, target):
    if(all(card is None for card in game.field.p1_st_zone) and all(card is None for card in game.field.p2_st_zone)):
        return False

    return True


def de_spell(game, card, target):
    owner = card.current_owner
    available_targets = []

    for card in game.p1.st_zone:
        if(card is None):
            continue
        if(card.face_up and card.card_type == 'spell'):
            available_targets.append(card)
        elif(not card.face_up):
            available_targets.append(card)

    for card in game.p2.st_zone:
        if(card is None):
            continue
        if(card.face_up and card.card_type == 'spell'):
            available_targets.append(card)
        elif(not card.face_up):
            available_targets.append(card)

    target = mechanics.choose_card(available_targets, owner)
    # target(target)

    if(not target.face_up):
        mechanics.reveal(target)

    if(target.card_type == 'spell'):
        mechanics.destroy(game, target)


def change_of_heart_condition(game, card, target):
    opponent = card.current_owner.opponent
    if(all(card is None for card in opponent.monster_zone)):
        return False

    return True


def change_of_heart(game, card, target):
    opponent = card.current_owner.opponent
    available_targets = []
    for monster in opponent.monster_zone:
        if monster is not None:
            available_targets.append(monster)

    target = mechanics.choose_card(available_targets, card.current_owner)
    # target(target)

    idx = target.location.index(target)
    target.location[idx] = None

    zone = summon.choose_zone(card.current_owner)
    card.current_owner.monster_zone[zone] = target
    target.location = card.current_owner.monster_zone

    game.effects.append({
        'card': card,
        'check': 'end phase',
        'turnActivated': game.turn_counter,
        'end phase': change_of_heart_end_effect,
        'target': target,
        'target player': opponent,
        'location': target.location,
        'original location': opponent.monster_zone,
    })


def change_of_heart_end_effect(effect_info, game):
    target = effect_info['target']
    if(game.turn_counter is not effect_info['turnActivated']):
        return

    if(target.location is not effect_info['location']):
        return

    zone = summon.choose_zone(effect_info['target player'])

    idx = target.location.index(target)
    target.location[idx] = None

    effect_info['original location'][zone] = target
    target.location = effect_info['original location']
    game.effects.remove(effect_info)
