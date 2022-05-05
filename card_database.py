from monster import Monster
from trap import Trap
from spell import Spell
from effect import Effect
import spell_effects
import trap_effects
import monster_effects


def getCard(cardName):
    database = {
        'Summoned Skull': summonedSkull,
        'La Jinn the Mystical Genie of the Lamp': laJinn,
        'Neo the Magic Swordsman': neoMagicSwordsman,
        'Battle Ox': battleOx,
        'Wall of Illusion': wallOfIllusion,
        'Giant Soldier of Stone': giantSoldier,
        'Trap Master': trapMaster,
        'Man-Eater Bug': manEaterBug,
        'Pot of Greed': potOfGreed,
        'Monster Reborn': monsterReborn,
        'Raigeki': raigeki,
        'Dark Hole': darkHole,
        'Change of Heart': changeOfHeart,
        'De-Spell': deSpell,
        'Fissure': fissure,
        'Swords of Revealing Light': swordsOfRevealing,
        'Reinforcements': reinforcements,
        'Trap Hole': trapHole,
        'Waboku': waboku,
        'Just Desserts': justDesserts
    }

    card = database[cardName]

    return card()


def summonedSkull():
    return Monster(name='Summoned Skull', attack=2500, defense=1200, level=6, monsterType=['Fiend', 'Normal'], attribute='Dark', effect=None)


def laJinn():
    return Monster(name='La Jinn the Mystical Genie of the Lamp', attack=1800, defense=1000, level=4, monsterType=['Fiend', 'Normal'], attribute='Dark', effect=None)


def neoMagicSwordsman():
    return Monster(name='Neo the Magic Swordsman', attack=1700, defense=1000, level=4, monsterType=['Spellcaster', 'Normal'], attribute='Light', effect=None)


def battleOx():
    return Monster(name='Battle Ox', attack=1700, defense=1000, level=4, monsterType=['Beast-Warrior', 'Normal'], attribute='Earth', effect=None)


def wallOfIllusion():
    effect = Effect(effect=monster_effects.wallOfIllusion, cost=None,
                    condition=None, trigger=['Continuous'], responses=[None], effectType=['Trigger'], initial=monster_effects.wallOfIllusion)

    return Monster(name='Wall of Illusion', attack=1000, defense=1850, level=4, monsterType=['Fiend', 'Effect'], attribute='Dark', effect=effect)


def giantSoldier():
    return Monster(name='Giant Soldier of Stone', attack=1300, defense=2000, level=3, monsterType=['Rock', 'Normal'], attribute='Earth', effect=None)


def trapMaster():
    effect = Effect(effect=monster_effects.trapMaster, cost=None,
                    condition=monster_effects.trapMasterCondition, trigger=['Flip'], responses=['Any', 'Destroy trap'], effectType=['Flip'])

    return Monster(name='Trap Master', attack=500, defense=1100, level=3, monsterType=['Warrior', 'Flip', 'Effect'], attribute='Earth', effect=effect)


def manEaterBug():
    effect = Effect(effect=monster_effects.manEaterBug, cost=None,
                    condition=monster_effects.manEaterBugCondition, trigger=['Flip'], responses=['Any', 'Destroy monster'], effectType=['Flip'])

    return Monster(name='Man-Eater Bug', attack=450, defense=600, level=2, monsterType=['Insect', 'Flip', 'Effect'], attribute='Earth', effect=effect)


def potOfGreed():
    effect = Effect(effect=spell_effects.potOfGreed,
                    cost=None, condition=None, trigger=None, responses=['Any', 'Draw cards', 'Activate spell'], effectType=['Effect'])

    return Spell(name='Pot of Greed', effect=effect, spellType='Normal', spellSpeed=1)


def monsterReborn():
    effect = Effect(effect=spell_effects.monsterReborn, cost=None,
                    condition=spell_effects.monsterRebornCondition, trigger=None, responses=['Any', 'Special summon monster', 'Activate spell'], effectType=['Effect'])

    return Spell(name='Monster Reborn', effect=effect, spellType='Normal', spellSpeed=1)


def raigeki():
    effect = Effect(effect=spell_effects.raigeki, cost=None,
                    condition=spell_effects.raigekiCondition, trigger=None, responses=['Any', 'Destroy monster', 'Activate spell'], effectType=['Effect'])

    return Spell(name='Raigeki', effect=effect, spellType='Normal', spellSpeed=1)


def darkHole():
    effect = Effect(effect=spell_effects.darkHole, cost=None,
                    condition=spell_effects.darkHoleCondition, trigger=None, responses=['Any', 'Send monster to graveyard', 'Activate spell'], effectType=['Effect'])

    return Spell(name='Dark Hole', effect=effect, spellType='Normal', spellSpeed=1)


def changeOfHeart():
    effect = Effect(effect=spell_effects.changeOfHeart, cost=None,
                    condition=spell_effects.changeOfHeartCondition, trigger=None, responses=['Any', 'Activate spell'], effectType=['Effect'])

    return Spell(name='Change of Heart', effect=effect, spellType='Normal', spellSpeed=1)


def deSpell():
    effect = Effect(effect=spell_effects.deSpell, cost=None,
                    condition=spell_effects.deSpellCondition, trigger=None, responses=['Any', 'Activate spell', 'Destroy spell'], effectType=['Effect'])

    return Spell(name='De-Spell', effect=effect, spellType='Normal', spellSpeed=1)


def fissure():
    effect = Effect(effect=spell_effects.fissure, cost=None,
                    condition=spell_effects.fissureCondition, trigger=None, responses=['Any', 'Activate spell', 'Destroy monster'], effectType=['Effect'])

    return Spell(name='Fissure', effect=effect, spellType='Normal', spellSpeed=1)


def swordsOfRevealing():
    effect = Effect(effect=spell_effects.swordsOfRevealingLight,
                    cost=None, condition=None, trigger=None, responses=['Any', 'Activate spell'], effectType=['Condition', 'Effect', 'Continuous-like'])

    return Spell(name='Swords Of Revealing Light', effect=effect, spellType='Continuous-like', spellSpeed=1)


def reinforcements():
    effect = Effect(effect=trap_effects.reinforcements, cost=None,
                    condition=trap_effects.reinforcementsCondition, trigger=['Any', 'modify atk/def'], responses=['Any', 'Activate trap', 'Modify atk/def'], effectType=['Effect'])

    return Trap(name='Reinforcements', effect=effect, trapType='Normal', spellSpeed=2)


def trapHole():
    effect = Effect(effect=trap_effects.trapHole, cost=None, condition=trap_effects.trapHoleCondition, trigger=[
                    'When Opponent Normal Summons', 'When Opponent Flip Summons'], responses=['Any', 'Activate trap', 'Destroy monster'], effectType=['Activation requirement', 'Effect'])

    return Trap(name='Trap Hole', effect=effect, trapType='Normal', spellSpeed=2)


def waboku():
    effect = Effect(effect=trap_effects.waboku, cost=None,
                    condition=None, trigger=['Any'], responses=['Any', 'Activate trap'], effectType=['Effect'])

    return Trap(name='Waboku', effect=effect, trapType='Normal', spellSpeed=2)


def justDesserts():
    effect = Effect(effect=trap_effects.justDesserts, cost=None,
                    condition=trap_effects.justDessertsCondition, trigger=['Any'], responses=['Any', 'Activate trap', 'Inflict damage'], effectType=['Effect'])

    return Trap(name='Just Desserts', effect=effect, trapType='Normal', spellSpeed=2)
