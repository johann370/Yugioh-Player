from Card import Card
from Summon import summon


class Monster(Card):
    def __init__(self, name, attack, defense, level, monsterType, attribute):
        super().__init__(name, "monster")
        self.attack = attack
        self.defense = defense
        self.position = None
        self.level = level
        self.monsterType = monsterType
        self.attribute = attribute
        self.options = ['Normal Summon', 'Set']
