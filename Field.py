class Field:
    def __init__(self):
        self.p1MonsterZone = [None] * 5
        self.p2MonsterZone = [None] * 5
        self.extraMonsterZone = [None] * 2
        self.p1STZone = [None] * 5
        self.p2STZone = [None] * 5
        self.p1FieldSpell = [None]
        self.p2FieldSpell = [None]

    def __str__(self) -> str:
        string = ''

        for monster in self.p2MonsterZone:
            if (monster is None):
                string += ' | None'
            elif (monster.faceUp):
                string += ' | ' + monster.name + ' (' + monster.position + ')'
            else:
                string += ' | Face Down Monster' + \
                    ' (' + monster.position + ')'

        string += '\n-------------------------------------------------------\n'

        for monster in self.p1MonsterZone:
            if (monster is None):
                string += ' | None'
            elif (monster.faceUp):
                string += ' | ' + monster.name + ' (' + monster.position + ')'
            else:
                string += ' | Face Down Monster' + \
                    ' (' + monster.position + ')'

        return string
