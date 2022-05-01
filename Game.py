from Field import Field
from Monster import Monster
from Player import Player
from Summon import summon
import Mechanics


class Game():
    card = Monster('Gem-Knight Garnet', 1900, 0,
                   4, 'Pyro/Normal', 'Earth', effect=None)
    card2 = Monster('Test', 2000, 1900, 4, 'Pyro/Normal', 'Earth', effect=None)
    card3 = Monster('High Level Monster', 3000, 2500,
                    7, 'Normal', 'Light', effect=None)
    deck = [card] * 5
    deck.append(card3)
    deck2 = [card2] * 5
    p1 = Player('p1', deck, 8000)
    p2 = Player('p2', deck2, 8000)
    p1.opponent = p2
    p2.opponent = p1
    field = Field(p1, p2)
    effects = []
    turnCounter = 1
    turnPlayer = p1
    otherPlayer = p2
    battle = {'attacker': None, 'defender': None}
    normalSummonUsed = False
    chain = None

    def __init__(self):
        pass

    def test(self):
        self.p1.deck.shuffle()
        self.p1.deck.draw(4)
        self.p2.deck.draw(5)

        while(True):
            self.turn()

    def startGame(self):
        self.p1.deck.shuffle()
        self.p1.deck.draw(5)
        self.p2.deck.shuffle()
        self.p2.deck.draw(5)

    def turn(self):
        self.drawPhase()
        self.standbyPhase()
        self.mainPhase1()
        self.battlePhase()
        self.mainPhase2()
        self.endPhase()

    def drawPhase(self):
        print(f'{self.turnPlayer.name} turn (Turn {self.turnCounter})\n')
        print('Draw Phase\n')
        self.turnPlayer.deck.draw(1)

    def standbyPhase(self):
        print('Standby Phase\n')
        pass

    def mainPhase1(self):
        print('Main Phase 1\n')

        while(True):
            print('1. Next phase \n2. Select Card\n3. Print Hand\n4. Print Field')
            val = int(input('Choose Option: '))
            if(val == 1):
                return
            elif(val == 2):
                card = Mechanics.chooseCard(self.turnPlayer.hand.cards)
                self.selectCard(card)
            elif(val == 3):
                self.turnPlayer.hand.printHand()
            elif(val == 4):
                print(self.field)

    def battlePhase(self):
        if(self.turnCounter == 1):
            return

        print('Battle Phase\n')

        availableAttackers = []
        for monster in self.turnPlayer.monsterZone:
            if (monster is not None and not monster.hasAttacked):
                availableAttackers.append(monster)

        attacker = Mechanics.chooseCard(availableAttackers)

        availableTargets = []
        for monster in self.otherPlayer.monsterZone:
            if (monster is not None):
                availableTargets.append(monster)

        if(not availableTargets):
            availableTargets.append(self.otherPlayer)

        target = Mechanics.chooseCard(availableTargets)

        self.declareAttack(attacker, target)

    def mainPhase2(self):
        print('Main Phase 2\n')

        while(True):
            print('1. Next phase \n2. Select Card\n3. Print Hand\n4. Print Field')
            val = int(input('Choose Option: '))
            if(val == 1):
                return
            elif(val == 2):
                card = Mechanics.chooseCard(self.turnPlayer.hand.cards)
                self.selectCard(card)
            elif(val == 3):
                self.turnPlayer.hand.printHand()
            elif(val == 4):
                print(self.field)

    def endPhase(self):
        print('End Phase\n')

        self.checkEffects('end of turn')

        temp = self.turnPlayer
        self.turnPlayer = self.otherPlayer
        self.otherPlayer = temp
        self.turnCounter += 1

    def selectCard(self, card):
        options = card.getOptions(self)
        print('Options: ')
        for i in range(len(options)):
            print(f'{i}. {options[i]}')
        val = int(input('Choose an option: '))
        self.chooseOption(card, options[val])

    def chooseOption(self, card, option):
        if (option == 'Normal Summon'):
            summon('normal', card, self)
            self.checkFaceDowns(
                self.otherPlayer, 'When Opponent Normal Summons')
        elif (option == 'Set Monster'):
            summon('set', card, self)
        elif (option == 'Tribute Summon'):
            summon('tribute', card, self)
            self.checkFaceDowns(
                self.otherPlayer, 'When Opponent Normal Summons')
        elif (option == 'Flip Summon'):
            summon('flip', card, self)
            self.checkFaceDowns(self.otherPlayer, 'When Opponent Flip Summons')
        elif (option == 'Change Battle Position'):
            Mechanics.changeBattlePosition(card, self)
        elif (option == 'Activate'):
            Mechanics.createChain(self, card)
        elif (option == 'Set'):
            pass

    def declareAttack(self, monster, target):
        self.battle['attacker'] = monster
        self.battle['defender'] = target
        self.damageStep(monster, target)

    def damageStep(self, monster, target):
        # Start of Damage Step
        self.checkFaceDowns(self.turnPlayer, 'modify atk/def')
        self.checkFaceDowns(self.otherPlayer, 'modify atk/def')

        # Before damage calculation
        if(not target.faceUp):
            target.faceUp = True

        self.checkFaceDowns(self.turnPlayer, 'modify atk/def')
        self.checkFaceDowns(self.otherPlayer, 'modify atk/def')

        # Perform damage calculation
        self.performDamageCalculation(monster, target)

        # After damage calculation
        self.checkEffects('after damage calculation')
        if('Flip' in target.monsterType):
            Mechanics.activateCard(target, self)

        # End of Damage Step
        if(target.position == 'attack'):
            if(monster.attack > target.attack):
                Mechanics.destroyByBattle(target)
            elif(monster.attack < target.attack):
                Mechanics.destroyByBattle(monster)
            elif(monster.attack == target.attack):
                Mechanics.destroyByBattle(monster)
                Mechanics.destroyByBattle(target)
        elif(target.position == 'defense'):
            if(monster.attack > target.defense):
                Mechanics.destroyByBattle(target)
            elif(monster.attack < target.defense):
                pass
            elif(monster.attack == target.defense):
                pass

    def performDamageCalculation(self, monster, target):
        if(target.position == 'attack'):
            if(monster.attack > target.attack):
                self.inflictBattleDamage(target.currentOwner,
                                         monster.attack - target.attack)
            elif(monster.attack < target.attack):
                self.inflictBattleDamage(monster.currentOwner,
                                         target.attack - monster.attack)
        elif(target.position == 'defense'):
            if(monster.attack < target.defense):
                self.inflictBattleDamage(monster.currentOwner,
                                         target.defense - monster.attack)

    def inflictBattleDamage(self, player, damageAmount):
        if('No battle damage taken' in player.effects):
            return

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

    def checkFaceDowns(self, player, trigger):
        cardsToPick = []
        for card in player.STZone:
            if(card is not None and trigger in card.effect.trigger):
                cardsToPick.append(card)

    def prompt(self, player, cards):
        pass
