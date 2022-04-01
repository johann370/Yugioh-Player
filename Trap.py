from Card import Card


class Trap(Card):
    def __init__(self, name, effect, trapType, spellSpeed):
        super().__init__(name, 'trap')
        self.effect = effect
        self.trapType = trapType
        self.spellSpeed = spellSpeed
        self.turnSet = None
        self.options = ['Set']
