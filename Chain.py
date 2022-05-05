from chain_link import ChainLink
import mechanics


class Chain:
    def __init__(self) -> None:
        self.chain = []
        self.spellSpeed = 1
        self.cards = []

    def resolve(self, game):
        cards = []
        while(self.chain):
            chainLink = self.chain.pop()
            chainLink.card.effect.activate(
                game, chainLink.card, chainLink.previousCard)
            if('Continuous-like' not in chainLink.card.effect.effectType and chainLink.card.cardType != 'monster'):
                cards.append(chainLink.card)

        mechanics.sendToGrave(cards)

    def addChainLink(self, card, previousCard):
        chainLink = ChainLink(card, previousCard)
        self.chain.append(chainLink)
        self.cards.append(card)
