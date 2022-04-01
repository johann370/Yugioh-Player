import Mechanics


def potOfGreed(player):
    Mechanics.draw(player, 2)


def raigeki(opponent):
    for monster in opponent.monsterZone:
        Mechanics.destroy(monster)
