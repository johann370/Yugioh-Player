from Mechanics import tribute


def summon(summonType, monster, player, field):
    if(summonType == 'normal'):
        normalSummon(monster, player, field)
    elif(summonType == 'set'):
        set(monster, player, field)
    elif(summonType == 'flip'):
        flipSummon(monster)
    elif(summonType == 'tribute'):
        tributeSummon(monster, player, field)


def chooseZone(player):
    availableZones = []

    for i in range(len(player.monsterZone)):
        if(player.monsterZone[i] is None):
            availableZones.append(i)

    print(f'Available zones: {availableZones}')
    zone = int(input('Choose a zone: '))

    while(zone not in availableZones):
        print(f'Available zones: {availableZones}')
        zone = int(input('Invalid zone, please choose a zone: '))

    return zone


def normalSummon(monster, player, field):
    zone = chooseZone(player)
    if(player.name == 'p1'):
        player.hand.cards.remove(monster)
        monster.position = 'attack'
        monster.faceUp = True
        field.p1MonsterZone[zone] = monster
    else:
        player.hand.cards.remove(monster)
        monster.position = 'attack'
        monster.faceUp = True
        field.p2MonsterZone[zone] = monster


def set(monster, player, field):
    zone = chooseZone(player)
    if(player.name == 'p1'):
        player.hand.cards.remove(monster)
        monster.position = 'defense'
        monster.faceUp = False
        field.p1MonsterZone[zone] = monster
    else:
        player.hand.cards.remove(monster)
        monster.position = 'defense'
        monster.faceUp = False
        field.p2MonsterZone[zone] = monster


def flipSummon(monster):
    monster.position = 'attack'
    monster.faceUp = True


def tributeSummon(monster, player, field):
    numOfTributes = 1
    if(monster.level >= 7):
        numOfTributes = 2

    monstersToTribute = []
    availableZones = []
    for i in range(len(player.monsterZone)):
        if(player.monsterZone[i] is not None):
            availableZones.append(i)

    for i in range(numOfTributes):
        for i in availableZones:
            print(f'{i}. {player.monsterZone[i].name}')
        zoneOfTribute = int(input('Choose a monster to tribute: '))

        while(zoneOfTribute not in availableZones):
            for i in availableZones:
                print(f'{i}. {player.monsterZone[i].name}')
            zoneOfTribute = int(input('Invalid zone, please choose a zone: '))

        availableZones.remove(zoneOfTribute)
        monsterTribute = player.monsterZone[zoneOfTribute]
        monstersToTribute.append(monsterTribute)

    tribute(monstersToTribute, field)

    position = int(input('Choose battle position: \n1. Attack \n2. Defense\n'))
    while(position is not 1 and position is not 2):
        position = int(
            input('Choose battle position: \n1. Attack \n2. Defense\n'))

    if(position == 1):
        normalSummon(monster, player, field)
    elif(position == 2):
        set(monster, player, field)
