from Mechanics import tribute


def summon(summonType, monster, game):
    if(summonType == 'normal'):
        normalSummon(monster)
    elif(summonType == 'set'):
        set(monster)
    elif(summonType == 'flip'):
        flipSummon(monster)
    elif(summonType == 'tribute'):
        tributeSummon(monster)
    elif(summonType == 'special'):
        specialSummon(monster)

    monster.turnSummoned = game.turn
    monster.location = monster.currentOwner.monsterZone
    if(monster.effect is not None and monster.effect.initial is not None):
        monster.effect.initial(game, monster, None)


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


def normalSummon(monster):
    zone = chooseZone(monster.currentOwner)
    monster.currentOwner.hand.cards.remove(monster)
    monster.position = 'attack'
    monster.faceUp = True
    monster.currentOwner.monsterZone[zone] = monster


def set(monster):
    zone = chooseZone(monster.currentOwner)
    monster.currentOwner.hand.cards.remove(monster)
    monster.position = 'defense'
    monster.faceUp = False
    monster.currentOwner.monsterZone[zone] = monster


def flipSummon(monster):
    monster.position = 'attack'
    monster.faceUp = True


def tributeSummon(monster):
    player = monster.currentOwner
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

    tribute(monstersToTribute)

    position = int(input('Choose battle position: \n1. Attack \n2. Defense\n'))
    while(position != 1 and position != 2):
        position = int(
            input('Choose battle position: \n1. Attack \n2. Defense\n'))

    if(position == 1):
        normalSummon(monster)
    elif(position == 2):
        set(monster)


def specialSummon(monster):
    zone = chooseZone(monster.currentOwner)
    position = int(input('Choose battle position: \n1. Attack \n2. Defense\n'))
    while(position != 1 and position != 2):
        position = int(
            input('Choose battle position: \n1. Attack \n2. Defense\n'))

    if(position == 1):
        monster.position = 'attack'
    elif(position == 2):
        monster.position = 'defense'

    monster.faceUp = True
    monster.location.cards.remove(monster)
    monster.currentOwner.monsterZone[zone] = monster
