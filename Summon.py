def summon(summonType, monster, zone, player, field):
    if(summonType == 'normal'):
        normalSummon(monster, zone, player, field)


def normalSummon(monster, zone, player, field):
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
