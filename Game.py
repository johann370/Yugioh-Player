from Field import Field
from Monster import Monster
from Player import Player
from Summon import summon
from Mechanics import destroy


class Game():
    card = Monster('Gem-Knight Garnet', 1900, 0,
                   4, 'Pyro/Normal', 'Earth')
    card2 = Monster('Test', 2000, 1900, 4, 'Pyro/Normal', 'Earth')
    card3 = Monster('High Level Monster', 3000, 2500, 7, 'Normal', 'Light')
    deck = [card] * 5
    deck.append(card3)
    deck2 = [card2] * 5
    p1 = Player('p1', deck, 8000)
    p2 = Player('p2', deck2, 8000)
    field = Field(p1, p2)
    turn = 1
    effects = []
    turnPlayer = p1
    otherPlayer = p2

    def __init__(self):
        pass

    def test(self):
        self.p1.deck.shuffle()
        self.p1.deck.draw(4)
        self.p2.deck.draw(5)
        self.turn(self.p1)
        summon('set', self.p2.hand.cards[0], self.p2, self.field)
        summon('normal', self.p1.hand.cards[0], self.p1, self.field)
        print('\n')
        print(self.field)
        print('\n')
        self.declareAttack(
            self.field.p1MonsterZone[0], self.field.p2MonsterZone[0])
        print(self.field)
        print(f'Player 1 LP: {self.p1.lp}')
        print(f'Player 2 LP: {self.p2.lp}')

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
        self.checkEffects('end of turn')

    def chooseCard(self, card, player):
        print('Options: ')
        for i in range(len(card.options)):
            print(f'{i}. {card.options[i]}')
        val = int(input('Choose an option: '))
        self.chooseOption(card, card.options[val], player)

    def chooseOption(self, card, option):
        if (option == 'Normal Summon'):
            summon('normal', card, self)
            self.checkFaceDowns(
                self.otherPlayer, 'When Opponent Normal Summons')
        elif (option == 'Set'):
            summon('set', card, self)
        elif (option == 'Tribute Summon'):
            summon('tribute', card, self)
            self.checkFaceDowns(
                self.otherPlayer, 'When Opponent Normal Summons')
        elif (option == 'Flip Summon'):
            summon('flip', card, self)
            self.checkFaceDowns(self.otherPlayer, 'When Opponent Flip Summon')

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

    def declareAttack(self, monster, target):
        self.damageStep(monster, target)

    def damageStep(self, monster, target):
        # Start of Damage Step

        # Before damage calculation
        if(not target.faceUp):
            target.faceUp = True

        # Perform damage calculation
        self.performDamageCalculation(monster, target)

        # After damage calculation

        # End of Damage Step
        if(target.position == 'attack'):
            if(monster.attack > target.attack):
                destroy(target, self.field)
            elif(monster.attack < target.attack):
                destroy(monster, self.field)
            elif(monster.attack == target.attack):
                destroy(monster, self.field)
                destroy(target, self.field)
        elif(target.position == 'defense'):
            if(monster.attack > target.defense):
                destroy(target, self.field)
            elif(monster.attack < target.defense):
                pass
            elif(monster.attack == target.defense):
                pass

    def performDamageCalculation(self, monster, target):
        if(target.position == 'attack'):
            if(monster.attack > target.attack):
                self.inflictDamage(target.currentOwner,
                                   monster.attack - target.attack)
            elif(monster.attack < target.attack):
                self.inflictDamage(monster.currentOwner,
                                   target.attack - monster.attack)
        elif(target.position == 'defense'):
            if(monster.attack < target.defense):
                self.inflictDamage(monster.currentOwner,
                                   target.defense - monster.attack)

    def inflictDamage(self, player, damageAmount):
        player.lp -= damageAmount
        self.checkWin()

    def checkWin(self):
        if(self.p1.lp > 0 and self.p2.lp > 0):
            return

        if(self.p1.lp <= 0):
            print('Player 2 Wins!')
        elif(self.p2.lp <= 0):
            print('Player 1 Wins!')

    def checkEffects(self, check):
        if (not self.effects):
            return

        for effect in self.effects:
            if(effect['check'] == check):
                effect['end effect'](effect, self)
                self.effects.remove(effect)

    def checkFaceDowns(player, trigger):
        cardsToPick = []
        for card in player.STZone:
            if(card.effect.trigger == trigger):
                cardsToPick.append(card)

    def prompt(player, cards):
        pass
