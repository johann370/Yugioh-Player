from Monster import Monster
from Trap import Trap
from Spell import Spell
from Effect import Effect
import SpellEffects
import TrapEffects
import MonsterEffects


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
    effect = Effect(effect=MonsterEffects.wallOfIllusion, cost=None,
                    condition=None, trigger=['Continuous'], responses=[None])

    return Monster(name='Wall of Illusion', attack=1000, defense=1850, level=4, monsterType=['Fiend', 'Effect'], attribute='Dark', effect=effect)


def giantSoldier():
    return Monster(name='Giant Soldier of Stone', attack=1300, defense=2000, level=3, monsterType=['Rock', 'Normal'], attribute='Earth', effect=None)


def trapMaster():
    effect = Effect(effect=MonsterEffects.trapMaster, cost=None,
                    condition=MonsterEffects.trapMasterCondition, trigger=['Flip'], responses=['Any', 'Destroy trap'])

    return Monster(name='Trap Master', attack=500, defense=1100, level=3, monsterType=['Warrior', 'Flip', 'Effect'], attribute='Earth', effect=effect)


def manEaterBug():
    pass


def potOfGreed():
    effect = Effect(effect=SpellEffects.potOfGreed,
                    cost=None, condition=None, trigger=None, responses=['Any', 'Draw cards', 'Activate spell'])

    return Spell(name='Pot of Greed', effect=effect, spellType='Normal', spellSpeed=1)


def monsterReborn():
    effect = Effect(effect=SpellEffects.monsterReborn, cost=None,
                    condition=SpellEffects.monsterRebornCondition, trigger=None, responses=['Any', 'Special summon monster', 'Activate spell'])

    return Spell(name='Monster Reborn', effect=effect, spellType='Normal', spellSpeed=1)


def raigeki():
    effect = Effect(effect=SpellEffects.raigeki, cost=None,
                    condition=SpellEffects.raigekiCondition, trigger=None, responses=['Any', 'Destroy monster', 'Activate spell'])

    return Spell(name='Raigeki', effect=effect, spellType='Normal', spellSpeed=1)


def darkHole():
    effect = Effect(effect=SpellEffects.darkHole, cost=None,
                    condition=SpellEffects.darkHoleCondition, trigger=None, responses=['Any', 'Send monster to graveyard', 'Activate spell'])

    return Spell(name='Dark Hole', effect=effect, spellType='Normal', spellSpeed=1)


def changeOfHeart():
    effect = Effect(effect=SpellEffects.changeOfHeart, cost=None,
                    condition=SpellEffects.changeOfHeartCondition, trigger=None, responses=['Any', 'Activate spell'])

    return Spell(name='Change of Heart', effect=effect, spellType='Normal', spellSpeed=1)


def deSpell():
    effect = Effect(effect=SpellEffects.deSpell, cost=None,
                    condition=SpellEffects.deSpellCondition, trigger=None, responses=['Any', 'Activate spell', 'Destroy spell'])

    return Spell(name='De-Spell', effect=effect, spellType='Normal', spellSpeed=1)


def fissure():
    effect = Effect(effect=SpellEffects.fissure, cost=None,
                    condition=SpellEffects.fissureCondition, trigger=None, responses=['Any', 'Activate spell', 'Destroy monster'])

    return Spell(name='Fissure', effect=effect, spellType='Normal', spellSpeed=1)


def swordsOfRevealing():
    effect = Effect(effect=SpellEffects.swordsOfRevealingLight,
                    cost=None, condition=None, trigger=None, responses=['Any', 'Activate spell'])

    return Spell(name='Swords Of Revealing Light', effect=effect, spellType='Normal', spellSpeed=1)


def reinforcements():
    effect = Effect(effect=TrapEffects.reinforcements, cost=None,
                    condition=TrapEffects.reinforcementsCondition, trigger=['Any', 'modify atk/def'], responses=['Any', 'Activate trap', 'Modify atk/def'])

    return Trap(name='Reinforcements', effect=effect, trapType='Normal', spellSpeed=2)


def trapHole():
    effect = Effect(effect=TrapEffects.trapHole, cost=None, condition=TrapEffects.trapHoleCondition, trigger=[
                    'When Opponent Normal Summons', 'When Opponent Flip Summons'], responses=['Any', 'Activate trap', 'Destroy monster'])

    return Trap(name='Trap Hole', effect=effect, trapType='Normal', spellSpeed=2)


def waboku():
    effect = Effect(effect=TrapEffects.waboku, cost=None,
                    condition=None, trigger=['Any'], responses=['Any', 'Activate trap'])

    return Trap(name='Waboku', effect=effect, trapType='Normal', spellSpeed=2)


def justDesserts():
    effect = Effect(effect=TrapEffects.justDesserts, cost=None,
                    condition=TrapEffects.justDessertsCondition, trigger=['Any'], responses=['Any', 'Activate trap', 'Inflict damage'])

    return Trap(name='Just Desserts', effect=effect, trapType='Normal', spellSpeed=2)