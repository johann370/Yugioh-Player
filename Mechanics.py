from chain import Chain
from dataclasses import Field, field

from player import Player


def destroy_by_battle(game, monster):
    if('Monsters not destroyed by battle' in monster.current_owner.effects):
        return

    destroy(game, monster)


def destroy(game, card):
    if card is None:
        return
    elif(card not in card.current_owner.monster_zone and card not in card.current_owner.st_zone):
        return

    idx = card.location.index(card)
    card.location[idx] = None
    card.owner.graveyard.cards.append(card)
    card.location = card.owner.graveyard.cards

    for effect in game.effects:
        if(effect['card'] == card and 'end effect' in effect):
            effect['end effect'](effect, game)


def tribute(cards):
    for card in cards:
        card.current_owner.monster_zone.remove(card)
        card.owner.graveyard.add(card)


def draw(player, num_of_cards):
    return player.deck.draw(num_of_cards)


def set_card(card):
    zone = choose_zone(card.current_owner.st_zone)
    card.face_up = False
    card.current_owner.hand.cards.remove(card)
    card.current_owner.st_zone[zone] = card
    card.location = card.current_owner.st_zone


def change_battle_position(monster, game):
    if(monster.last_turn_position_changed == game.turn_counter or monster.turn_summoned == game.turn_counter):
        return

    if(monster.position == 'attack'):
        monster.position = 'defense'
    elif(monster.position == 'defense'):
        monster.position = 'attack'
        if(not monster.face_up):
            flip(monster)
    monster.last_turn_position_changed = game.turn_counter


def inflict_battle_damage(player, damage_amount):
    if('No battle damage taken' in player.effects):
        return

    inflict_damage(player, damage_amount)


def inflict_damage(player, amount):
    player.lp -= amount


def activate_card(game, card):
    if(game.chain is None):
        create_chain(game, card)


def flip(game, monster):
    monster.face_up = True
    if('Flip' in monster.monster_type):
        create_chain(game, monster, None)


def choose_card(options, player):
    for i in range(len(options)):
        if(options[i] is not None):
            if(isinstance(options[i], Player)):
                print(f'{i}. {options[i].name}')
            elif(options[i].face_up is None or options[i].face_up or options[i].current_owner == player):
                print(
                    f'{i}. {options[i].name} ({options[i].current_owner.name})')
            elif(not options[i].face_up):
                print(f'{i}. Face Down ({options[i].current_owner.name})')
        elif(options[i] is None):
            print(f'{i}. Cancel')

    value = int(input('Choose card: '))

    while(value < 0 and value > len(options)):
        value = int(input('Choose valid card: '))

    return options[value]


def reveal(card):
    print(card.name)


def check_for_response(game, player, responses, previous_card):
    if(all(card is None for card in player.st_zone)):
        return False

    available_cards = []

    for card in player.st_zone:
        if card is None:
            continue
        if(game.chain is not None and card.spell_speed < game.chain.spell_speed):
            continue
        if(card == previous_card):
            continue
        if(game.chain is not None and card in game.chain.cards):
            continue
        for response in responses:
            if(card.effect.trigger is None) or response not in card.effect.trigger:
                continue
            elif (card.effect.condition is None or card.effect.condition(game, card, previous_card) and card not in available_cards):
                available_cards.append(card)

    if (not available_cards):
        return False

    available_cards.append(None)

    response = choose_card(available_cards, player)

    if (response is None):
        return False

    if(game.chain is None):
        create_chain(game, response, previous_card)
    else:
        add_to_chain(game, response, previous_card)

    return True


def create_chain(game, card, previous_card):
    if(game.chain and not game.chain.cards):
        return

    game.chain = Chain()
    add_to_chain(game, card, previous_card)
    game.chain.resolve(game)
    game.chain = None


def add_to_chain(game, card, previous_card):
    card.effect.pay_cost()
    game.chain.addChainLink(card, previous_card)

    response = check_for_response(
        game, card.current_owner.opponent, card.effect.responses, card)

    if(not response):
        check_for_response(game, card.current_owner,
                           card.effect.responses, card)


def target_monster(cards):
    monster_on_field = []

    for i in range(len(Field.p1Monster+Field.p2Monster)):
        monster_on_field.append(i)

    print(f'monsters on field: {monster_on_field}')
    target = int(input('Target Monster'))

    while(target not in monster_on_field):
        print(f'monsters on field: {monster_on_field}')
        target = int(input('Target Monster'))

    return target


def choose_zone(zone):
    available_zones = []

    for i in range(len(zone)):
        if(zone[i] is None):
            available_zones.append(i)

    print(f'Available zones: {available_zones}')
    zone_num = int(input('Choose a zone: '))

    while(zone_num not in available_zones):
        print(f'Available zones: {available_zones}')
        zone_num = int(input('Invalid zone, please choose a zone: '))

    return zone_num


def send_to_grave(cards):
    if(not cards):
        return

    for card in cards:
        idx = card.location.index(card)
        card.location[idx] = None
        card.owner.graveyard.cards.append(card)
        card.location = card.owner.graveyard.cards


def prompt(player, cards):
    card = choose_card(cards, player)

    return card
