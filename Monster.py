from card import Card
from summon import summon


class Monster(Card):
    def __init__(self, name, attack, defense, level, monster_type, attribute, effect):
        super().__init__(name, "monster")
        self.original_attack = attack
        self.attack = attack
        self.original_defense = defense
        self.defense = defense
        self.position = None
        self.level = level
        self.monster_type = monster_type
        self.attribute = attribute
        self.last_turn_position_changed = None
        self.turn_summoned = None
        self.can_declare_attack = True
        self.effect = effect
        self.has_attacked = False

    def get_options(self, game, monster):
        available_options = []

        if(game.normal_summon_used):
            return available_options

        zone_full = True
        num_of_monsters = 0
        for card in self.current_owner.monster_zone:
            if card is None:
                zone_full = False
            else:
                num_of_monsters += 1

        if (zone_full and self.level <= 4):
            return available_options

        if(self.level <= 4 and self.turn_summoned is None):
            available_options = ['Normal Summon', 'Set Monster']
        elif(self.level > 4 and self.level < 7 and self.turn_summoned is None and num_of_monsters >= 1):
            available_options = ['Tribute Summon']
        elif(self.level >= 7 and self.turn_summoned is None and num_of_monsters >= 2):
            available_options = ['Tribute Summon']

        if(not self.face_up and self.turn_summoned is not None and game.turn_counter != self.turn_summoned):
            available_options = ['Flip Summon']

        if(self.turn_summoned is not None and game.turn_counter != self.last_turn_position_changed and self.face_up):
            available_options = ['Change Battle Position']

        return available_options
