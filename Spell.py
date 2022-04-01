from Card import Card


class Spell(Card):
    def __init__(self, name, effect, spellType, spellSpeed):
        super().__init__(name, 'spell')
        self.effect = effect
        self.spellType = spellType
        self.spellSpeed = spellSpeed
        self.turnSet = None
        self.options = ['Activate', 'Set']
