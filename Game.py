from Field import Field
from Monster import Monster
from Player import Player
from Summon import summon


class Game():
    field = Field()
    card = Monster('Gem-Knight Garnet', 1900, 0,
                   4, 'Pyro/Normal', 'Earth')
    deck = [card] * 5
    deck2 = [card] * 5
    p1 = Player('p1', deck, 8000)
    p2 = Player('p2', deck2, 8000)

    def __init__(self):
        pass

    def test(self):
        self.p1.deck.draw(2)
        self.p2.deck.draw(5)
        summon('normal', self.p2.hand.cards[0], 0, self.p2, self.field)
        summon('set', self.p1.hand.cards[0], 0, self.p1, self.field)
        print(self.field)

    def startGame(self):
        self.p1.deck.shuffle()
        self.p1.deck.draw(5)
        self.p2.deck.shuffle()
        self.p2.deck.draw(5)
        for card in self.p1.deck.cards:
            print(card)
        print(self.p1.hand.cards)

    def turn(self, player):
        self.drawPhase(player)
        self.standbyPhase(player)
        self.mainPhase1(player)
        self.battlePhase(player)
        self.mainPhase2(player)
        self.endPhase(player)

    def drawPhase(self, player):
        player.deck.draw(1)

    def standbyPhase(self, player):
        pass

    def mainPhase1(self, player):
        print('-1. Next phase')
        for i in range(len(player.hand.cards)):
            print(f'{i}. {player.hand.cards[i].name}')
        val = int(input('Choose a card: '))
        while(val >= 0):
            card = player.hand.cards[val]
            self.chooseCard(card, player)
            print('-1. Next phase')
            for i in range(len(player.hand.cards)):
                print(f'{i}. {player.hand.cards[i].name}')
            val = int(input('Choose a card: '))

    def battlePhase(self, player):
        pass

    def mainPhase2(self, player):
        print('-1. Next phase')
        for i in range(len(player.hand.cards)):
            print(f'{i}. {player.hand.cards[i].name}')
        val = int(input('Choose a card: '))
        while(val >= 0):
            card = player.hand.cards[val]
            self.chooseCard(card, player)
            print('-1. Next phase')
            for i in range(len(player.hand.cards)):
                print(f'{i}. {player.hand.cards[i].name}')
            val = int(input('Choose a card: '))

    def endPhase(self, player):
        pass

    def chooseCard(self, card, player):
        print('Options: ')
        for i in range(len(card.options)):
            print(f'{i}. {card.options[i]}')
        val = int(input('Choose an option: '))
        self.chooseOption(card, card.options[val], player)

    def chooseOption(self, card, option, player):
        if option == 'Normal Summon':
            zone = self.chooseZone('monster', player)
            summon('normal', card, zone, player, self.field)

    def chooseZone(self, zoneType, player):
        availableZones = []

        if(player.name == 'p1'):
            if (zoneType == 'monster'):
                for i in range(len(self.field.p1MonsterZone)):
                    if(self.field.p1MonsterZone[i] is None):
                        availableZones.append(i)
        else:
            if (zoneType == 'monster'):
                for i in range(len(self.field.p2MonsterZone)):
                    if(self.field.p2MonsterZone[i] is None):
                        availableZones.append(i)

        print(f'Available zones: {availableZones}')
        zone = int(input('Choose a zone: '))

        while(zone not in availableZones):
            print(f'Available zones: {availableZones}')
            zone = int(input('Invalid zone, please choose a zone: '))

        return zone
