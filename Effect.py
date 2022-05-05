class Effect():
    def __init__(self, effect, cost, condition, trigger, responses, effect_type, initial=None) -> None:
        self.effect = effect
        self.cost = cost
        self.condition = condition
        self.trigger = trigger
        self.responses = responses
        self.effect_type = effect_type
        self.initial = initial

    def activate(self, game, card, previous_card):
        if(self.condition is not None and not self.condition(game, card, previous_card)):
            return

        self.effect(game, card, previous_card)

    def pay_cost(self):
        if(self.cost is None):
            return

        self.cost()

    def check_condition(self, game, card, previous_card):
        if(self.condition is None):
            return True

        return self.condition(game, card, previous_card)
