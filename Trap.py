from Card import Card


class Trap(Card):
    def __init__(self, name, effect, spellType, spellSpeed):
        super().__init__(name, 'trap')
        self.effect = effect
        self.spellType = spellType
        self.spellSpeed = spellSpeed
        self.turnSet = None
        self.options = ['Set']
