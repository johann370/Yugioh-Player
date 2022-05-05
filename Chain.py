from chain_link import ChainLink
import mechanics


class Chain:
    def __init__(self) -> None:
        self.chain = []
        self.spell_speed = 1
        self.cards = []

    def resolve(self, game):
        cards = []
        while(self.chain):
            chain_link = self.chain.pop()
            chain_link.card.effect.activate(
                game, chain_link.card, chain_link.previous_card)
            if('Continuous-like' not in chain_link.card.effect.effect_type and chain_link.card.card_type != 'monster'):
                cards.append(chain_link.card)

        mechanics.send_to_grave(cards)

    def add_chain_link(self, card, previous_card):
        chain_link = ChainLink(card, previous_card)
        self.chain.append(chain_link)
        self.cards.append(card)
