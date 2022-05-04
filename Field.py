class Field:
    def __init__(self, p1, p2):
        self.p1MonsterZone = p1.monsterZone
        self.p2MonsterZone = p2.monsterZone
        self.extraMonsterZone = [None] * 2
        self.p1STZone = p1.STZone
        self.p2STZone = p2.STZone
        self.p1FieldSpell = p1.fieldSpell
        self.p2FieldSpell = p2.fieldSpell

    def __str__(self) -> str:
        string = ''

        for card in self.p2STZone:
            if(card is None):
                string += ' | None'
            elif(card.faceUp):
                string += ' | ' + card.name
            else:
                string += ' | Face Down Card'

        string += '\n'

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

        string += '\n'

        for card in self.p1STZone:
            if(card is None):
                string += ' | None'
            elif(card.faceUp):
                string += ' | ' + card.name
            else:
                string += ' | Face Down Card'

        return string
