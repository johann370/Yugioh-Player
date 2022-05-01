class Effect():
    def __init__(self, effect, cost, condition, trigger, responses) -> None:
        self.effect = effect
        self.cost = cost
        self.condition = condition
        self.trigger = trigger
        self.responses = responses

    def activate(self, card, game):
        if(self.condition is not None and not self.condition()):
            return

        self.effect()

    def payCost(self):
        if(self.cost is None):
            return

        self.cost()

    def checkCondition(self):
        if(self.condition is None):
            return True

        return self.condition()
