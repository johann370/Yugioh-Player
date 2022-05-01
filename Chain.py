from ChainLink import ChainLink


class Chain:
    def __init__(self) -> None:
        self.chain = []
        self.spellSpeed = 1

    def resolve(self):
        while(self.chain):
            chainLink = self.chain.pop()
            chainLink.card.effect.activate()

    def addChainLink(self, card):
        chainLink = ChainLink(card)
        self.chain.append(chainLink)
