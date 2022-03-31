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
        if(self.level <= 4):
            self.options = ['Normal Summon', 'Set']
        else:
            self.options = ['Tribute Summon', 'Set']
