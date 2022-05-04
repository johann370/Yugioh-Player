from ChainLink import ChainLink
import Mechanics


class Chain:
    def __init__(self) -> None:
        self.chain = []
        self.spellSpeed = 1

    def resolve(self, game):
        cards = []
        while(self.chain):
            chainLink = self.chain.pop()
            chainLink.card.effect.activate(
                game, chainLink.card, chainLink.previousCard)
            if('Continuous-like' not in chainLink.card.effect.effectType):
                cards.append(chainLink.card)

        Mechanics.sendToGrave(cards)

    def addChainLink(self, card, previousCard):
        chainLink = ChainLink(card, previousCard)
        self.chain.append(chainLink)
