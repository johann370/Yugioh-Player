class Effect():
    def __init__(self, effect, cost, condition, trigger) -> None:
        self.effect = effect
        self.cost = cost
        self.condition = condition
        self.trigger = trigger

    def activate(self):
        if(self.condition is not None and not self.condition()):
            return

        self.cost()
        self.effect()
