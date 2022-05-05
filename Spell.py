from card import Card


class Spell(Card):
    def __init__(self, name, effect, spell_type, spell_speed):
        super().__init__(name, 'spell')
        self.effect = effect
        self.spell_type = spell_type
        self.spell_speed = spell_speed
        self.turn_set = None

    def get_options(self, game, activated_card):
        available_options = []

        zone_full = True
        for card in self.current_owner.st_zone:
            if card is None:
                zone_full = False

        if (zone_full):
            return available_options

        if(self.effect.condition is None or self.effect.check_condition(game, activated_card, None)):
            available_options.append('Activate')

        if(self.turn_set is None):
            available_options.append('Set')

        return available_options
