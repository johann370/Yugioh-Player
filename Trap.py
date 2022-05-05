from card import Card


class Trap(Card):
    def __init__(self, name, effect, trap_type, spell_speed):
        super().__init__(name, 'trap')
        self.effect = effect
        self.trap_type = trap_type
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

        if(self.turn_set is not None and self.effect.check_condition(game, activated_card, None) and self.turn_set != game.turn_counter):
            available_options.append('Activate')

        if(self.turn_set is None):
            available_options.append('Set')

        return available_options
