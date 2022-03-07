import Card


class Monster(Card):
    def __init__(self, name, attack, defense, position, level, type, attribute):
        super().__init__(name, "monster")
        self.attack = attack
        self.defense = defense
        self.position = position
        self.level = level
        self.type = type
        self.attribute = attribute

    def attack(target):
        pass
