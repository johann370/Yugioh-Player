class Effect():
    def __init__(self, effect, cost, condition, trigger, responses, effectType, initial=None) -> None:
        self.effect = effect
        self.cost = cost
        self.condition = condition
        self.trigger = trigger
        self.responses = responses
        self.effectType = effectType
        self.initial = initial

    def activate(self, game, card, previousCard):
        if(self.condition is not None and not self.condition(game, card, previousCard)):
            return

        self.effect(game, card, previousCard)

    def payCost(self):
        if(self.cost is None):
            return

        self.cost()

    def checkCondition(self, game, card, previousCard):
        if(self.condition is None):
            return True

        return self.condition(game, card, previousCard)
