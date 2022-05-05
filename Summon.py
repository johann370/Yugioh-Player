from mechanics import tribute, flip


def summon(summon_type, monster, game):
    if(summon_type == 'normal'):
        normal_summon(monster)
    elif(summon_type == 'set'):
        set(monster)
    elif(summon_type == 'flip'):
        flip_summon(game, monster)
    elif(summon_type == 'tribute'):
        tribute_summon(monster)
    elif(summon_type == 'special'):
        special_summon(monster)

    monster.turn_summoned = game.turn_counter
    monster.location = monster.current_owner.monster_zone
    if(monster.effect is not None and monster.effect.initial is not None):
        monster.effect.initial(game, monster, None)


def choose_zone(player):
    available_zones = []

    for i in range(len(player.monster_zone)):
        if(player.monster_zone[i] is None):
            available_zones.append(i)

    print(f'Available zones: {available_zones}')
    zone = int(input('Choose a zone: '))

    while(zone not in available_zones):
        print(f'Available zones: {available_zones}')
        zone = int(input('Invalid zone, please choose a zone: '))

    return zone


def normal_summon(monster):
    zone = choose_zone(monster.current_owner)
    monster.current_owner.hand.cards.remove(monster)
    monster.position = 'attack'
    monster.face_up = True
    monster.current_owner.monster_zone[zone] = monster


def set(monster):
    zone = choose_zone(monster.current_owner)
    monster.current_owner.hand.cards.remove(monster)
    monster.position = 'defense'
    monster.face_up = False
    monster.current_owner.monster_zone[zone] = monster


def flip_summon(game, monster):
    monster.position = 'attack'
    flip(game, monster)


def tribute_summon(monster):
    player = monster.current_owner
    num_of_tributes = 1
    if(monster.level >= 7):
        num_of_tributes = 2

    monsters_to_tribute = []
    available_zones = []
    for i in range(len(player.monster_zone)):
        if(player.monster_zone[i] is not None):
            available_zones.append(i)

    for i in range(num_of_tributes):
        for i in available_zones:
            print(f'{i}. {player.monster_zone[i].name}')
        zone_of_tribute = int(input('Choose a monster to tribute: '))

        while(zone_of_tribute not in available_zones):
            for i in available_zones:
                print(f'{i}. {player.monster_zone[i].name}')
            zone_of_tribute = int(
                input('Invalid zone, please choose a zone: '))

        available_zones.remove(zone_of_tribute)
        monster_tribute = player.monster_zone[zone_of_tribute]
        monsters_to_tribute.append(monster_tribute)

    tribute(monsters_to_tribute)

    position = int(input('Choose battle position: \n1. Attack \n2. Defense\n'))
    while(position != 1 and position != 2):
        position = int(
            input('Choose battle position: \n1. Attack \n2. Defense\n'))

    if(position == 1):
        normal_summon(monster)
    elif(position == 2):
        set(monster)


def special_summon(monster):
    zone = choose_zone(monster.current_owner)
    position = int(input('Choose battle position: \n1. Attack \n2. Defense\n'))
    while(position != 1 and position != 2):
        position = int(
            input('Choose battle position: \n1. Attack \n2. Defense\n'))

    if(position == 1):
        monster.position = 'attack'
    elif(position == 2):
        monster.position = 'defense'

    monster.face_up = True
    monster.location.cards.remove(monster)
    monster.current_owner.monster_zone[zone] = monster
