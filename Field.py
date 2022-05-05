class Field:
    def __init__(self, p1, p2):
        self.p1_monster_zone = p1.monster_zone
        self.p2_monster_zone = p2.monster_zone
        self.extra_monster_zone = [None] * 2
        self.p1_st_zone = p1.st_zone
        self.p2_st_zone = p2.st_zone
        self.p1_field_spell = p1.field_spell
        self.p2_field_spell = p2.field_spell

    def __str__(self) -> str:
        string = ''

        for card in self.p2_st_zone:
            if(card is None):
                string += ' | None'
            elif(card.face_up):
                string += ' | ' + card.name
            else:
                string += ' | Face Down Card'

        string += '\n'

        for monster in self.p2_monster_zone:
            if (monster is None):
                string += ' | None'
            elif (monster.face_up):
                string += ' | ' + monster.name + ' (' + monster.position + ')'
            else:
                string += ' | Face Down Monster' + \
                    ' (' + monster.position + ')'

        string += '\n-------------------------------------------------------\n'

        for monster in self.p1_monster_zone:
            if (monster is None):
                string += ' | None'
            elif (monster.face_up):
                string += ' | ' + monster.name + ' (' + monster.position + ')'
            else:
                string += ' | Face Down Monster' + \
                    ' (' + monster.position + ')'

        string += '\n'

        for card in self.p1_st_zone:
            if(card is None):
                string += ' | None'
            elif(card.face_up):
                string += ' | ' + card.name
            else:
                string += ' | Face Down Card'

        return string
