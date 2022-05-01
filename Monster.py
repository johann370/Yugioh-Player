from Card import Card
from Summon import summon


class Monster(Card):
    def __init__(self, name, attack, defense, level, monsterType, attribute, effect):
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
        self.effect = effect
        self.hasAttacked = False

    def getOptions(self, game):
        availableOptions = []

        if(game.normalSummonUsed):
            return availableOptions

        zoneFull = True
        for card in self.currentOwner.monsterZone:
            if card is None:
                zoneFull = False

        if (zoneFull and self.level <= 4):
            return availableOptions

        if(self.level <= 4 and self.turnSummoned is None):
            availableOptions = ['Normal Summon', 'Set Monster']
        elif(self.level > 4 and self.turnSummoned is None):
            availableOptions = ['Tribute Summon', 'Set Monster']

        if(not self.faceUp and self.turnSummoned is not None and game.turn != self.turnSummoned):
            availableOptions = ['Flip Summon']

        if(self.turnSummoned is not None and game.turn != self.lastTurnPositionChanged and self.faceUp):
            availableOptions = ['Change Battle Position']

        return availableOptions
