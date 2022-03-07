from Card import Card


class Monster(Card):
    def __init__(self, name, attack, defense, position, level, monsterType, attribute):
        super().__init__(name, "monster")
        self.attack = attack
        self.defense = defense
        self.position = position
        self.level = level
        self.monsterType = monsterType
        self.attribute = attribute

    def attack(target):
        pass
