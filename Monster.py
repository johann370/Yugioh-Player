from Card import Card
from Summon import summon


class Monster(Card):
    def __init__(self, name, attack, defense, level, monsterType, attribute):
        super().__init__(name, "monster")
        self.originalAttack = attack
        self.attack = attack
        self.originalDefense = defense
        self.defense = defense
        self.position = None
        self.level = level
        self.monsterType = monsterType
        self.attribute = attribute
        self.lastTurnPositionChanged = None
        self.turnSummoned = None
        self.canDeclareAttack = True
        if(self.level <= 4):
            self.options = ['Normal Summon', 'Set']
        else:
            self.options = ['Tribute Summon', 'Set']
