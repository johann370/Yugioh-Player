from monster import Monster
from trap import Trap
from spell import Spell
from effect import Effect
import spell_effects
import trap_effects
import monster_effects


def get_card(card_name):
    database = {
        'Summoned Skull': summoned_skull,
        'La Jinn the Mystical Genie of the Lamp': la_jinn,
        'Neo the Magic Swordsman': neo_magic_swordsman,
        'Battle Ox': battle_ox,
        'Wall of Illusion': wall_of_illusion,
        'Giant Soldier of Stone': giant_soldier,
        'Trap Master': trap_master,
        'Man-Eater Bug': man_eater_bug,
        'Pot of Greed': pot_of_greed,
        'Monster Reborn': monster_reborn,
        'Raigeki': raigeki,
        'Dark Hole': dark_hole,
        'Change of Heart': change_of_heart,
        'De-Spell': de_spell,
        'Fissure': fissure,
        'Swords of Revealing Light': swords_of_revealing,
        'Reinforcements': reinforcements,
        'Trap Hole': trap_hole,
        'Waboku': waboku,
        'Just Desserts': just_desserts
    }

    card = database[card_name]

    return card()


def summoned_skull():
    return Monster(name='Summoned Skull', attack=2500, defense=1200, level=6, monster_type=['Fiend', 'Normal'], attribute='Dark', effect=None)


def la_jinn():
    return Monster(name='La Jinn the Mystical Genie of the Lamp', attack=1800, defense=1000, level=4, monster_type=['Fiend', 'Normal'], attribute='Dark', effect=None)


def neo_magic_swordsman():
    return Monster(name='Neo the Magic Swordsman', attack=1700, defense=1000, level=4, monster_type=['Spellcaster', 'Normal'], attribute='Light', effect=None)


def battle_ox():
    return Monster(name='Battle Ox', attack=1700, defense=1000, level=4, monster_type=['Beast-Warrior', 'Normal'], attribute='Earth', effect=None)


def wall_of_illusion():
    effect = Effect(effect=monster_effects.wall_of_illusion, cost=None,
                    condition=None, trigger=['Continuous'], responses=[None], effect_type=['Trigger'], initial=monster_effects.wall_of_illusion)

    return Monster(name='Wall of Illusion', attack=1000, defense=1850, level=4, monster_type=['Fiend', 'Effect'], attribute='Dark', effect=effect)


def giant_soldier():
    return Monster(name='Giant Soldier of Stone', attack=1300, defense=2000, level=3, monster_type=['Rock', 'Normal'], attribute='Earth', effect=None)


def trap_master():
    effect = Effect(effect=monster_effects.trap_master, cost=None,
                    condition=monster_effects.trap_master_condition, trigger=['Flip'], responses=['Any', 'Destroy trap'], effect_type=['Flip'])

    return Monster(name='Trap Master', attack=500, defense=1100, level=3, monster_type=['Warrior', 'Flip', 'Effect'], attribute='Earth', effect=effect)


def man_eater_bug():
    effect = Effect(effect=monster_effects.man_eater_bug, cost=None,
                    condition=monster_effects.man_eater_bug_condition, trigger=['Flip'], responses=['Any', 'Destroy monster'], effect_type=['Flip'])

    return Monster(name='Man-Eater Bug', attack=450, defense=600, level=2, monster_type=['Insect', 'Flip', 'Effect'], attribute='Earth', effect=effect)


def pot_of_greed():
    effect = Effect(effect=spell_effects.pot_of_greed,
                    cost=None, condition=None, trigger=None, responses=['Any', 'Draw cards', 'Activate spell'], effect_type=['Effect'])

    return Spell(name='Pot of Greed', effect=effect, spell_type='Normal', spell_speed=1)


def monster_reborn():
    effect = Effect(effect=spell_effects.monster_reborn, cost=None,
                    condition=spell_effects.monster_reborn_condition, trigger=None, responses=['Any', 'Special summon monster', 'Activate spell'], effect_type=['Effect'])

    return Spell(name='Monster Reborn', effect=effect, spell_type='Normal', spell_speed=1)


def raigeki():
    effect = Effect(effect=spell_effects.raigeki, cost=None,
                    condition=spell_effects.raigeki_condition, trigger=None, responses=['Any', 'Destroy monster', 'Activate spell'], effect_type=['Effect'])

    return Spell(name='Raigeki', effect=effect, spell_type='Normal', spell_speed=1)


def dark_hole():
    effect = Effect(effect=spell_effects.dark_hole, cost=None,
                    condition=spell_effects.dark_hole_condition, trigger=None, responses=['Any', 'Send monster to graveyard', 'Activate spell'], effect_type=['Effect'])

    return Spell(name='Dark Hole', effect=effect, spell_type='Normal', spell_speed=1)


def change_of_heart():
    effect = Effect(effect=spell_effects.change_of_heart, cost=None,
                    condition=spell_effects.change_of_heart_condition, trigger=None, responses=['Any', 'Activate spell'], effect_type=['Effect'])

    return Spell(name='Change of Heart', effect=effect, spell_type='Normal', spell_speed=1)


def de_spell():
    effect = Effect(effect=spell_effects.de_spell, cost=None,
                    condition=spell_effects.de_spell_condition, trigger=None, responses=['Any', 'Activate spell', 'Destroy spell'], effect_type=['Effect'])

    return Spell(name='De-Spell', effect=effect, spell_type='Normal', spell_speed=1)


def fissure():
    effect = Effect(effect=spell_effects.fissure, cost=None,
                    condition=spell_effects.fissure_condition, trigger=None, responses=['Any', 'Activate spell', 'Destroy monster'], effect_type=['Effect'])

    return Spell(name='Fissure', effect=effect, spell_type='Normal', spell_speed=1)


def swords_of_revealing():
    effect = Effect(effect=spell_effects.swords_of_revealing_light,
                    cost=None, condition=None, trigger=None, responses=['Any', 'Activate spell'], effect_type=['Condition', 'Effect', 'Continuous-like'])

    return Spell(name='Swords Of Revealing Light', effect=effect, spell_type='Continuous-like', spell_speed=1)


def reinforcements():
    effect = Effect(effect=trap_effects.reinforcements, cost=None,
                    condition=trap_effects.reinforcements_condition, trigger=['Any', 'modify atk/def'], responses=['Any', 'Activate trap', 'Modify atk/def'], effect_type=['Effect'])

    return Trap(name='Reinforcements', effect=effect, trap_type='Normal', spell_speed=2)


def trap_hole():
    effect = Effect(effect=trap_effects.trap_hole, cost=None, condition=trap_effects.trap_hole_condition, trigger=[
                    'When Opponent Normal Summons', 'When Opponent Flip Summons'], responses=['Any', 'Activate trap', 'Destroy monster'], effect_type=['Activation requirement', 'Effect'])

    return Trap(name='Trap Hole', effect=effect, trap_type='Normal', spell_speed=2)


def waboku():
    effect = Effect(effect=trap_effects.waboku, cost=None,
                    condition=None, trigger=['Any'], responses=['Any', 'Activate trap'], effect_type=['Effect'])

    return Trap(name='Waboku', effect=effect, trap_type='Normal', spell_speed=2)


def just_desserts():
    effect = Effect(effect=trap_effects.just_desserts, cost=None,
                    condition=trap_effects.just_desserts_condition, trigger=['Any'], responses=['Any', 'Activate trap', 'Inflict damage'], effect_type=['Effect'])

    return Trap(name='Just Desserts', effect=effect, trap_type='Normal', spell_speed=2)
