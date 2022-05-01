from Card import Card


class Trap(Card):
    def __init__(self, name, effect, trapType, spellSpeed):
        super().__init__(name, 'trap')
        self.effect = effect
        self.trapType = trapType
        self.spellSpeed = spellSpeed
        self.turnSet = None

    def getOptions(self, game):
        availableOptions = []

        zoneFull = True
        for card in self.currentOwner.STZone:
            if card is None:
                zoneFull = False

        if (zoneFull):
            return availableOptions

        if(self.effect.condition() and self.turnSet != game.turn):
            availableOptions.append('Activate')

        if(self.turnSet is None):
            availableOptions.append('Set')

        return availableOptions
