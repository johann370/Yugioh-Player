from card import Card


class Spell(Card):
    def __init__(self, name, effect, spellType, spellSpeed):
        super().__init__(name, 'spell')
        self.effect = effect
        self.spellType = spellType
        self.spellSpeed = spellSpeed
        self.turnSet = None

    def getOptions(self, game, activatedCard):
        availableOptions = []

        zoneFull = True
        for card in self.currentOwner.STZone:
            if card is None:
                zoneFull = False

        if (zoneFull):
            return availableOptions

        if(self.effect.condition is None or self.effect.checkCondition(game, activatedCard, None)):
            availableOptions.append('Activate')

        if(self.turnSet is None):
            availableOptions.append('Set')

        return availableOptions
