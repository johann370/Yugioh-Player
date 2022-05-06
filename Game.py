from field import Field
from monster import Monster
from player import Player
from summon import summon
from create_deck import create_deck
import mechanics


class Game():
    # card = Monster('Gem-Knight Garnet', 1900, 0,
    #                4, 'Pyro/Normal', 'Earth', effect=None)
    # card2 = Monster('Test', 2000, 1900, 4, 'Pyro/Normal', 'Earth', effect=None)
    # card3 = Monster('High Level Monster', 3000, 2500,
    #                 7, 'Normal', 'Light', effect=None)
    deck = create_deck('Deck Lists\deck1.txt')
    deck2 = create_deck('Deck Lists\deck1.txt')
    p1 = Player('p1', deck, 8000)
    p2 = Player('p2', deck2, 8000)
    p1.opponent = p2
    p2.opponent = p1
    field = Field(p1, p2)
    effects = []
    turn_counter = 1
    turn_player = p1
    other_player = p2
    battle = {'attacker': None, 'defender': None}
    normal_summon_used = False
    chain = None
    monsters_attacked = []

    def __init__(self):
        pass

    def test(self):
        self.p1.deck.shuffle()
        self.p1.deck.draw(30)
        self.p2.deck.shuffle()
        self.p2.deck.draw(5)

        while(True):
            self.turn()

    def start_game(self):
        self.p1.deck.shuffle()
        self.p1.deck.draw(5)
        self.p2.deck.shuffle()
        self.p2.deck.draw(5)

        while(True):
            self.turn()

    def turn(self):
        self.draw_phase()
        self.standby_phase()
        self.main_phase(1)
        self.battle_phase()
        self.main_phase(2)
        self.end_phase()

    def draw_phase(self):
        print(f'{self.turn_player.name} turn (Turn {self.turn_counter})\n')
        print('Draw Phase\n')
        if(mechanics.draw(self.turn_player, 1) is None):
            self.end_game(self.other_player)

    def standby_phase(self):
        print('Standby Phase\n')
        pass

    def main_phase(self, num):
        print(f'Main Phase {num}')

        while(True):
            print(
                '\n1. Next phase \n2. Select Card In Hand\n3. Activate Set Card\n4. Print Hand\n5. Print Field\n6. Print Life Points\n7. Select Monster On Field')
            val = int(input('Choose Option: '))
            print('\n')
            if(val == 1):
                response = mechanics.check_for_response(
                    self, self.other_player, ['Any'], None)

                if(not response):
                    return
            elif(val == 2):
                card = mechanics.choose_card(
                    self.turn_player.hand.cards, self.turn_player)
                self.select_card(card)
            elif(val == 3):
                available_cards = []
                for card in self.turn_player.st_zone:
                    if(card is None):
                        continue
                    if(card.effect.condition is None or card.effect.condition(self, card, None)):
                        available_cards.append(card)

                available_cards.append(None)

                card_to_activate = mechanics.choose_card(
                    available_cards, self.turn_player)

                if(card_to_activate is None):
                    return

                mechanics.create_chain(self, card_to_activate, None)
            elif(val == 4):
                self.turn_player.hand.print_hand()
            elif(val == 5):
                print(f'\n{self.field}')
            elif(val == 6):
                print(f'P1: {self.p1.lp}\nP2: {self.p2.lp}')
            elif(val == 7):
                card = mechanics.choose_card(
                    self.turn_player.monster_zone, self.turn_player)

                if(card is None):
                    return

                self.select_card(card)

            self.check_effects('continuous effect')

    def battle_phase(self):
        if(self.turn_counter == 1):
            return

        print('Battle Phase\n')

        while(True):
            print('\n1. Declare Attack \n2. Activate Card\n3. End Battle Phase')
            val = int(input('Choose Option: '))
            print('\n')
            if(val == 1):
                available_attackers = []
                for monster in self.turn_player.monster_zone:
                    if (monster is not None and not monster.has_attacked and monster.position == 'attack' and monster.can_declare_attack):
                        available_attackers.append(monster)

                if (not available_attackers):
                    return

                available_attackers.append(None)

                attacker = mechanics.choose_card(
                    available_attackers, self.turn_player)

                if(attacker is None):
                    return

                available_targets = [
                    monster for monster in self.other_player.monster_zone if monster is not None]

                if(not available_targets):
                    available_targets.append(self.other_player)

                target = mechanics.choose_card(
                    available_targets, self.turn_player)

                if(target == self.p1 or target == self.p2):
                    self.declare_attack(attacker, target, True)
                else:
                    self.declare_attack(attacker, target, False)
            elif(val == 2):
                available_cards = [
                    card for card in self.turn_player.st_zone if card is not None and card.effect.check_condition(self, card, None) and card.spell_speed > 1]

                card_to_activate = mechanics.choose_card(
                    available_cards, self.turn_player)
                mechanics.create_chain(self, card_to_activate, None)
            elif(val == 3):
                response = mechanics.check_for_response(
                    self, self.other_player, ['Any'], None)

                if(not response):
                    return

    def end_phase(self):
        print('End Phase\n')

        self.check_effects('end phase')
        self.check_effects('end of turn')

        temp = self.turn_player
        self.turn_player = self.other_player
        self.other_player = temp
        self.turn_counter += 1
        self.normal_summon_used = False

        for monster in self.monsters_attacked:
            monster.has_attacked = False
        self.monsters_attacked = []

    def select_card(self, card):
        options = card.get_options(self, card)
        options.append('Cancel')
        print('Options: ')
        for idx, option in enumerate(options):
            print(f'{idx}. {option}')
        val = int(input('Choose an option: '))
        self.choose_option(card, options[val])

    def choose_option(self, card, option):
        if (option == 'Normal Summon'):
            summon('normal', card, self)
            self.normal_summon_used = True
            mechanics.check_for_response(self, self.other_player, [
                'When Opponent Normal Summons'], card)
        elif (option == 'Set Monster'):
            summon('set', card, self)
            self.normal_summon_used = True
        elif (option == 'Tribute Summon'):
            summon('tribute', card, self)
            self.normal_summon_used = True
            mechanics.check_for_response(self, self.other_player, [
                'When Opponent Normal Summons'], card)
        elif (option == 'Flip Summon'):
            summon('flip', card, self)
            mechanics.check_for_response(self, self.other_player, [
                'When Opponent Flip Summons'], card)
        elif (option == 'Change Battle Position'):
            mechanics.change_battle_position(card, self)
        elif (option == 'Activate'):
            zone = mechanics.choose_zone(card.current_owner.st_zone)
            card.location.remove(card)
            card.current_owner.st_zone[zone] = card
            card.location = card.current_owner.st_zone
            card.face_up = True
            mechanics.create_chain(self, card, None)
        elif (option == 'Set'):
            mechanics.set_card(card)
        elif (option == 'Cancel'):
            return

    def declare_attack(self, monster, target, direct_attack):
        monster.has_attacked = True
        self.monsters_attacked.append(monster)
        self.battle['attacker'] = monster
        self.battle['defender'] = target
        self.damage_step(monster, target, direct_attack)

    def damage_step(self, monster, target, direct_attack):
        # Start of Damage Step
        mechanics.check_for_response(self, self.turn_player, [
            'modify atk/def'], None)
        mechanics.check_for_response(self, self.other_player, [
            'modify atk/def'], None)

        # Before damage calculation
        if(not direct_attack and not target.face_up):
            target.face_up = True

        mechanics.check_for_response(self, self.turn_player, [
            'modify atk/def'], None)
        mechanics.check_for_response(self, self.other_player, [
            'modify atk/def'], None)

        # Perform damage calculation
        self.perform_damage_calculation(monster, target, direct_attack)

        # After damage calculation
        self.check_effects('after damage calculation')
        if(not direct_attack and 'Flip' in target.monster_type and not target.face_up):
            mechanics.create_chain(self, target, None)

        # End of Damage Step
        if(not direct_attack and target.position == 'attack'):
            if(monster.attack > target.attack):
                mechanics.destroy_by_battle(self, target)
            elif(monster.attack < target.attack):
                mechanics.destroy_by_battle(self, monster)
            elif(monster.attack == target.attack):
                mechanics.destroy_by_battle(self, monster)
                mechanics.destroy_by_battle(self, target)
        elif(not direct_attack and target.position == 'defense'):
            if(monster.attack > target.defense):
                mechanics.destroy_by_battle(self, target)
            elif(monster.attack < target.defense):
                pass
            elif(monster.attack == target.defense):
                pass

    def perform_damage_calculation(self, monster, target, direct_attack):
        if(direct_attack):
            mechanics.inflict_battle_damage(target, monster.attack)
            self.check_win()
            return

        if(target.position == 'attack'):
            if(monster.attack > target.attack):
                mechanics.inflict_battle_damage(target.current_owner,
                                                monster.attack - target.attack)
            elif(monster.attack < target.attack):
                mechanics.inflict_battle_damage(monster.current_owner,
                                                target.attack - monster.attack)
        elif(target.position == 'defense'):
            if(monster.attack < target.defense):
                mechanics.inflict_battle_damage(monster.current_owner,
                                                target.defense - monster.attack)

        self.check_win()

    def check_win(self):
        if(self.p1.lp > 0 and self.p2.lp > 0):
            return

        if(self.p1.lp <= 0):
            self.end_game(self.p2)
        elif(self.p2.lp <= 0):
            self.end_game(self.p1)

    def check_effects(self, check):
        if (not self.effects):
            return

        for effect in self.effects:
            if(check == effect['check']):
                effect[check](effect, self)
            elif(check in effect):
                effect[check](effect, self)

    def end_game(self, winner):
        print(f'{winner.name} wins!')
        quit()
