from enum import Enum
from Core.Hero import Hero

class ArenaFighter_Spell(Enum):
    NONE = 1
    LOSING_HEALTH = 2


_fighter_kinds = {}

def get_arena_fighter(name:str,hero: Hero)-> 'ArenaFighter' :
    if(str in hero):
       return _fighter_kinds[name](hero)
    else:
       return _fighter_kinds['generic'](hero)

class ArenaFighter:
    __slots__ = ('hero', 'health', 'affected_spell_value','affected_spell'
                 )

    def __init__(self, hero: Hero):
        self.hero[Hero] = hero
        self.health:[int] = 0
        self.affected_spell:ArenaFighter_Spell = ArenaFighter_Spell.NONE
        self.affected_spell_value:int = 0
        pass

    def reset(self):
        self.health = self.hero.health
        self.affected_spell = ArenaFighter_Spell.NONE
        pass

    def set_spell(self,affect_spell:ArenaFighter_Spell, value:int):
        self.affected_spell = affect_spell
        self.affected_spell_value = value
        pass

    def set_hit(self, damage:int):
        self.health -=damage

    def arena_round_start(self):
        pass

    def arena_round_end(self):
        pass

    def active_hero_start(self):
        pass

    def choose_targets(self, enemies: ['ArenaFighter'],teammates:['ArenaFighter'])->['ArenaFighter']:

        return next(_ for _ in enemies if id(_) != id(self))

    def hit_enemy(self, enemy: 'ArenaFighter'):
        pass

    def hit_friendly(self, enemy: 'ArenaFighter'):
        pass



    def active_hero_end(self):
        pass


class ArenaFighter_Zombie(ArenaFighter):

    def __init__(self, hero: Hero):
        super().__init__(hero)

    def arena_round_start(self):
        pass

    def arena_round_end(self):
        pass

    def active_hero_start(self):
        pass

    def choose_target(self, enemies: [ArenaFighter]):
        pass

    def hit_enemy(self, enemy: 'ArenaFighter'):
        pass

    def hit_friendly(self, enemy: 'ArenaFighter'):
        pass

    def active_hero_end(self):
        pass



_fighter_kinds['generic'] = ArenaFighter
_fighter_kinds['zombie'] = ArenaFighter_Zombie



if __name__ == "__main__":
    pass
