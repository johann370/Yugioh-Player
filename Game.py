from field import Field
from monster import Monster
from player import Player
from summon import summon
from create_deck import createDeck
import mechanics


class Game():
    # card = Monster('Gem-Knight Garnet', 1900, 0,
    #                4, 'Pyro/Normal', 'Earth', effect=None)
    # card2 = Monster('Test', 2000, 1900, 4, 'Pyro/Normal', 'Earth', effect=None)
    # card3 = Monster('High Level Monster', 3000, 2500,
    #                 7, 'Normal', 'Light', effect=None)
    deck = createDeck('Deck Lists\deck1.txt')
    deck2 = createDeck('Deck Lists\deck1.txt')
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
    monstersAttacked = []

    def __init__(self):
        pass

    def test(self):
        self.p1.deck.shuffle()
        self.p1.deck.draw(5)
        self.p2.deck.shuffle()
        self.p2.deck.draw(5)

        while(True):
            self.turn()

    def startGame(self):
        self.p1.deck.shuffle()
        self.p1.deck.draw(5)
        self.p2.deck.shuffle()
        self.p2.deck.draw(5)

        while(True):
            self.turn()

    def turn(self):
        self.drawPhase()
        self.standbyPhase()
        self.mainPhase(1)
        self.battlePhase()
        self.mainPhase(2)
        self.endPhase()

    def drawPhase(self):
        print(f'{self.turnPlayer.name} turn (Turn {self.turnCounter})\n')
        print('Draw Phase\n')
        if(mechanics.draw(self.turnPlayer, 1) is None):
            self.endGame(self.otherPlayer)

    def standbyPhase(self):
        print('Standby Phase\n')
        pass

    def mainPhase(self, num):
        print(f'Main Phase {num}')

        while(True):
            print(
                '\n1. Next phase \n2. Select Card In Hand\n3. Activate Set Card\n4. Print Hand\n5. Print Field\n6. Print Life Points\n7. Select Monster On Field')
            val = int(input('Choose Option: '))
            print('\n')
            if(val == 1):
                response = mechanics.checkForResponse(
                    self, self.otherPlayer, ['Any'], None)

                if(not response):
                    return
            elif(val == 2):
                card = mechanics.chooseCard(
                    self.turnPlayer.hand.cards, self.turnPlayer)
                self.selectCard(card)
            elif(val == 3):
                availableCards = []
                for card in self.turnPlayer.STZone:
                    if(card is None):
                        continue
                    if(card.effect.condition is None or card.effect.condition(self, card, None)):
                        availableCards.append(card)

                availableCards.append(None)

                cardToActivate = mechanics.chooseCard(
                    availableCards, self.turnPlayer)

                if(cardToActivate is None):
                    return

                mechanics.createChain(self, cardToActivate, None)
            elif(val == 4):
                self.turnPlayer.hand.printHand()
            elif(val == 5):
                print(f'\n{self.field}')
            elif(val == 6):
                print(f'P1: {self.p1.lp}\nP2: {self.p2.lp}')
            elif(val == 7):
                card = mechanics.chooseCard(
                    self.turnPlayer.monsterZone, self.turnPlayer)

                if(card is None):
                    return

                self.selectCard(card)

            self.checkEffects('continuousEffect')

    def battlePhase(self):
        if(self.turnCounter == 1):
            return

        print('Battle Phase\n')

        while(True):
            print('\n1. Declare Attack \n2. Activate Card\n3. End Battle Phase')
            val = int(input('Choose Option: '))
            print('\n')
            if(val == 1):
                availableAttackers = []
                for monster in self.turnPlayer.monsterZone:
                    if (monster is not None and not monster.hasAttacked and monster.position == 'attack' and monster.canDeclareAttack):
                        availableAttackers.append(monster)

                if (not availableAttackers):
                    return

                availableAttackers.append(None)

                attacker = mechanics.chooseCard(
                    availableAttackers, self.turnPlayer)

                if(attacker is None):
                    return

                availableTargets = []
                for monster in self.otherPlayer.monsterZone:
                    if (monster is not None):
                        availableTargets.append(monster)

                if(not availableTargets):
                    availableTargets.append(self.otherPlayer)

                target = mechanics.chooseCard(
                    availableTargets, self.turnPlayer)

                if(target == self.p1 or target == self.p2):
                    self.declareAttack(attacker, target, True)
                else:
                    self.declareAttack(attacker, target, False)
            elif(val == 2):
                availableCards = []
                for card in self.turnPlayer.STZone:
                    if(card is None):
                        continue
                    if(card.effect.condition(self, card, None)):
                        availableCards.append(card)

                cardToActivate = mechanics.chooseCard(
                    availableCards, self.turnPlayer)
                mechanics.createChain(self, cardToActivate, None)
            elif(val == 3):
                response = mechanics.checkForResponse(
                    self, self.otherPlayer, ['Any'], None)

                if(not response):
                    return

    def endPhase(self):
        print('End Phase\n')

        self.checkEffects('end phase')
        self.checkEffects('end of turn')

        temp = self.turnPlayer
        self.turnPlayer = self.otherPlayer
        self.otherPlayer = temp
        self.turnCounter += 1
        self.normalSummonUsed = False

        for monster in self.monstersAttacked:
            monster.hasAttacked = False
        self.monstersAttacked = []

    def selectCard(self, card):
        options = card.getOptions(self, card)
        options.append('Cancel')
        print('Options: ')
        for i in range(len(options)):
            print(f'{i}. {options[i]}')
        val = int(input('Choose an option: '))
        self.chooseOption(card, options[val])

    def chooseOption(self, card, option):
        if (option == 'Normal Summon'):
            summon('normal', card, self)
            self.normalSummonUsed = True
            mechanics.checkForResponse(self, self.otherPlayer, [
                                       'When Opponent Normal Summons'], card)
        elif (option == 'Set Monster'):
            summon('set', card, self)
            self.normalSummonUsed = True
        elif (option == 'Tribute Summon'):
            summon('tribute', card, self)
            self.normalSummonUsed = True
            mechanics.checkForResponse(self, self.otherPlayer, [
                                       'When Opponent Normal Summons'], card)
        elif (option == 'Flip Summon'):
            summon('flip', card, self)
            mechanics.checkForResponse(self, self.otherPlayer, [
                                       'When Opponent Flip Summons'], card)
        elif (option == 'Change Battle Position'):
            mechanics.changeBattlePosition(card, self)
        elif (option == 'Activate'):
            zone = mechanics.chooseZone(card.currentOwner.STZone)
            card.location.remove(card)
            card.currentOwner.STZone[zone] = card
            card.location = card.currentOwner.STZone
            card.faceUp = True
            mechanics.createChain(self, card, None)
        elif (option == 'Set'):
            mechanics.setCard(card)
        elif (option == 'Cancel'):
            return

    def declareAttack(self, monster, target, directAttack):
        monster.hasAttacked = True
        self.monstersAttacked.append(monster)
        self.battle['attacker'] = monster
        self.battle['defender'] = target
        self.damageStep(monster, target, directAttack)

    def damageStep(self, monster, target, directAttack):
        # Start of Damage Step
        mechanics.checkForResponse(self, self.turnPlayer, [
            'modify atk/def'], None)
        mechanics.checkForResponse(self, self.otherPlayer, [
            'modify atk/def'], None)

        # Before damage calculation
        if(not directAttack and not target.faceUp):
            target.faceUp = True

        mechanics.checkForResponse(self, self.turnPlayer, [
            'modify atk/def'], None)
        mechanics.checkForResponse(self, self.otherPlayer, [
            'modify atk/def'], None)

        # Perform damage calculation
        self.performDamageCalculation(monster, target, directAttack)

        # After damage calculation
        self.checkEffects('after damage calculation')
        if(not directAttack and 'Flip' in target.monsterType and not target.faceUp):
            mechanics.createChain(self, target, None)

        # End of Damage Step
        if(not directAttack and target.position == 'attack'):
            if(monster.attack > target.attack):
                mechanics.destroyByBattle(self, target)
            elif(monster.attack < target.attack):
                mechanics.destroyByBattle(self, monster)
            elif(monster.attack == target.attack):
                mechanics.destroyByBattle(self, monster)
                mechanics.destroyByBattle(self, target)
        elif(not directAttack and target.position == 'defense'):
            if(monster.attack > target.defense):
                mechanics.destroyByBattle(self, target)
            elif(monster.attack < target.defense):
                pass
            elif(monster.attack == target.defense):
                pass

    def performDamageCalculation(self, monster, target, directAttack):
        if(directAttack):
            mechanics.inflictBattleDamage(target, monster.attack)
            self.checkWin()
            return

        if(target.position == 'attack'):
            if(monster.attack > target.attack):
                mechanics.inflictBattleDamage(target.currentOwner,
                                              monster.attack - target.attack)
            elif(monster.attack < target.attack):
                mechanics.inflictBattleDamage(monster.currentOwner,
                                              target.attack - monster.attack)
        elif(target.position == 'defense'):
            if(monster.attack < target.defense):
                mechanics.inflictBattleDamage(monster.currentOwner,
                                              target.defense - monster.attack)

        self.checkWin()

    def checkWin(self):
        if(self.p1.lp > 0 and self.p2.lp > 0):
            return

        if(self.p1.lp <= 0):
            self.endGame(self.p2)
        elif(self.p2.lp <= 0):
            self.endGame(self.p1)

    def checkEffects(self, check):
        if (not self.effects):
            return

        for effect in self.effects:
            if(check == effect['check']):
                effect[check](effect, self)
            elif(check in effect):
                effect[check](effect, self)

    def endGame(self, winner):
        print(f'{winner.name} wins!')
        quit()
