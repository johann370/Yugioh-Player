from card import Card


class Trap(Card):
    def __init__(self, name, effect, trapType, spellSpeed):
        super().__init__(name, 'trap')
        self.effect = effect
        self.trapType = trapType
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

        if(self.turnSet is not None and self.effect.checkCondition(game, activatedCard, None) and self.turnSet != game.turnCounter):
            availableOptions.append('Activate')

        if(self.turnSet is None):
            availableOptions.append('Set')

        return availableOptions
