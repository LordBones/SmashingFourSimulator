from enum import Enum
from Core.Hero import Hero

class ArenaFighter_Spell(Enum):
    NONE = 1
    POISON_ZOMBIE = 2
    DECREASED_ATTACK = 3
    WIND_SPEED = 4

_fighter_kinds = {}

def get_arena_fighter(name:str,hero: Hero)-> 'ArenaFighter' :
    if(name in _fighter_kinds):
       return _fighter_kinds[name](hero)
    else:
       return _fighter_kinds['generic'](hero)

class ArenaFighter:
    __slots__ = ('hero', 'health', 'affected_spell_value','affected_spell','team_group'
                 )

    def __init__(self, hero: Hero):
        self.team_group = 0
        self.hero:[Hero] = hero
        self.health:[int] = 0
        self.affected_spell:ArenaFighter_Spell = ArenaFighter_Spell.NONE
        self.affected_spell_value:int = 0
        pass

    def reset(self):
        self.health = self.hero.health
        self.affected_spell = ArenaFighter_Spell.NONE
        self.affected_spell_value = 0
        pass

    def _get_modify_attack(self, attack:int)->int:

        tmp_attack = attack

        if(self.affected_spell == ArenaFighter_Spell.DECREASED_ATTACK):
            tmp_attack = tmp_attack - self.affected_spell_value

        return tmp_attack

    def set_spell(self,affect_spell:ArenaFighter_Spell, value:int):
        self.affected_spell = affect_spell
        self.affected_spell_value = value
        pass

    def set_hit(self, damage:int):
        if(damage > 0):
            self.health -=damage
        pass

    def arena_round_start(self):
        pass

    def arena_round_end(self, enemies: ['ArenaFighter']):

        if self.affected_spell == ArenaFighter_Spell.POISON_ZOMBIE:
            self.set_hit(self.affected_spell_value)

        pass

    def active_hero_start(self):
        pass

    def choose_targets(self, enemies: ['ArenaFighter'],teammates:['ArenaFighter'])->['ArenaFighter']:

        return [enemies[0]]

    def hit_enemy(self, enemy: 'ArenaFighter'):
        attack = self._get_modify_attack(self.hero.attack)
        enemy.set_hit(attack)
        pass

    def hit_friendly(self, enemy: 'ArenaFighter'):
        pass



    def active_hero_end(self,enemies: ['ArenaFighter']):
        pass


class ArenaFighter_Zombie(ArenaFighter):

    def __init__(self, hero: Hero):
        super().__init__(hero)
    pass




    def hit_enemy(self, enemy: 'ArenaFighter'):
        super().hit_enemy(enemy)
        enemy.set_spell( ArenaFighter_Spell.POISON_ZOMBIE, self.hero.ability)

        pass


class ArenaFighter_Strazce(ArenaFighter):

    def __init__(self, hero: Hero):
        super().__init__(hero)

    def hit_enemy(self, enemy: 'ArenaFighter'):
        attack = self._get_modify_attack(self.hero.ability)
        enemy.set_hit(attack)
        pass

class ArenaFighter_Dzin(ArenaFighter):
    def __init__(self, hero: Hero):
        super().__init__(hero)

    def hit_enemy(self, enemy: 'ArenaFighter'):
        attack= int((enemy.hero.health * self.hero.ability)/100)
        attack = self._get_modify_attack(attack)
        enemy.set_hit(attack)
        pass

class ArenaFighter_Bersek(ArenaFighter):
    def __init__(self, hero: Hero):
        super().__init__(hero)

    def hit_enemy(self, enemy: 'ArenaFighter'):

        attack=self.hero.attack
        if(self.health < (self.hero.health // 2)):
            attack += self.hero.ability

        attack = self._get_modify_attack(attack)
        enemy.set_hit(attack)
        pass

class ArenaFighter_Pirat(ArenaFighter):
    def __init__(self, hero: Hero):
        super().__init__(hero)

    def active_hero_start(self):
        self.health += self.hero.ability
        if(self.health > self.hero.health):
            self.health = self.hero.health
        pass

class ArenaFighter_Raketak(ArenaFighter):
    def __init__(self, hero: Hero):
        super().__init__(hero)

    def hit_enemy(self, enemy: 'ArenaFighter'):
        attack = self.hero.ability
        attack = self._get_modify_attack(attack)
        enemy.set_hit(attack)
        pass

class ArenaFighter_Rytir(ArenaFighter):
    __slots__ = ('hero', 'health', 'affected_spell_value', 'affected_spell', 'team_group', 'first_hit'
                 )

    def __init__(self, hero: Hero):
        super().__init__(hero)
        self.first_hit = False

    def active_hero_start(self):
        self.first_hit = False
        pass

    def set_hit(self, damage: int):
        tmp_damage = damage
        if (not self.first_hit):
            tmp_damage -= self.hero.ability
            self.first_hit = True

        tmp_damage = tmp_damage if tmp_damage >= 0 else 0

        self.health -= tmp_damage
        pass

class ArenaFighter_Golem(ArenaFighter):

    def __init__(self, hero: Hero):
        super().__init__(hero)

    def arena_round_end(self, enemies: ['ArenaFighter']):
        super().arena_round_end(enemies)
        attack = self._get_modify_attack(self.hero.ability)
        enemies[0].set_hit(attack)
        pass

class ArenaFighter_Goblin(ArenaFighter):

    def __init__(self, hero: Hero):
        super().__init__(hero)
        pass

    def hit_enemy(self, enemy: 'ArenaFighter'):
        attack = self.hero.ability + self.hero.attack
        attack = self._get_modify_attack(attack)
        enemy.set_hit(attack)
        pass

class ArenaFighter_Vampire(ArenaFighter):

    def __init__(self, hero: Hero):
        super().__init__(hero)
        pass

    def hit_enemy(self, enemy: 'ArenaFighter'):
        super().hit_enemy(enemy)

        self.health += self.hero.ability
        if (self.health > self.hero.health):
            self.health = self.hero.health

        pass

class ArenaFighter_Druid(ArenaFighter):

    def __init__(self, hero: Hero):
        super().__init__(hero)

    def arena_round_end(self, enemies: ['ArenaFighter']):
        super().arena_round_end(enemies)

        enemy = max(enemies,key=lambda x: x.health)
        attack = self._get_modify_attack(self.hero.ability)
        enemy.set_hit(attack)
        pass


class ArenaFighter_Saman(ArenaFighter):

    def __init__(self, hero: Hero):
        super().__init__(hero)

    def hit_enemy(self, enemy: 'ArenaFighter'):
        super().hit_enemy(enemy)

        enemy.set_spell( ArenaFighter_Spell.DECREASED_ATTACK,self.hero.ability)
        pass

class ArenaFighter_IceQueen(ArenaFighter):

    def __init__(self, hero: Hero):
        super().__init__(hero)

    def active_hero_end(self,enemies: ['ArenaFighter']):
        for enemy in enemies:
            attack = self._get_modify_attack(self.hero.ability)
            enemy.set_hit(attack)
        pass

class ArenaFighter_Wizard(ArenaFighter):

    def __init__(self, hero: Hero):
        super().__init__(hero)
        pass

    def hit_enemy(self, enemy: 'ArenaFighter'):
        remain_health = enemy.health

        super().hit_enemy(enemy)
        enemy.set_hit(  (remain_health * self.hero.ability) // 100 )

        pass

class ArenaFighter_Satyr(ArenaFighter):

    def __init__(self, hero: Hero):
        super().__init__(hero)
        pass

    def hit_enemy(self, enemy: 'ArenaFighter'):
        remain_health = enemy.health
        attack = self.hero.attack
        if(self.affected_spell != ArenaFighter_Spell.NONE):
            attack += self.hero.ability

        attack = self._get_modify_attack(attack)
        enemy.set_hit( attack )

        pass

class ArenaFighter_Pasovec(ArenaFighter):

    def __init__(self, hero: Hero):
        super().__init__(hero)
        pass

    def hit_enemy(self, enemy: 'ArenaFighter'):
        super().hit_enemy(enemy)
        if (enemy.affected_spell != ArenaFighter_Spell.NONE):
            enemy.set_spell(ArenaFighter_Spell.NONE,0)
            enemy.set_hit(self.hero.ability)


        pass

class ArenaFighter_Bansi(ArenaFighter):

    def __init__(self, hero: Hero):
        super().__init__(hero)
        pass

    def active_hero_start(self):
        self.set_spell(ArenaFighter_Spell.WIND_SPEED,0)
        pass

class ArenaFighter_Naga(ArenaFighter):

    def __init__(self, hero: Hero):
        super().__init__(hero)
        pass

    def hit_enemy(self, enemy: 'ArenaFighter'):
        super().hit_enemy(enemy)
        if (enemy.affected_spell != ArenaFighter_Spell.NONE):
            enemy.set_hit(self.hero.ability)


        pass



_fighter_kinds['generic'] = ArenaFighter
_fighter_kinds['zombie'] = ArenaFighter_Zombie
_fighter_kinds['strazce'] = ArenaFighter_Strazce
_fighter_kinds['dzin'] = ArenaFighter_Dzin
_fighter_kinds['bersek'] = ArenaFighter_Bersek
_fighter_kinds['pirat'] = ArenaFighter_Pirat
_fighter_kinds['raketak'] = ArenaFighter_Raketak
_fighter_kinds['rytir'] = ArenaFighter_Rytir
_fighter_kinds['golem'] = ArenaFighter_Golem
_fighter_kinds['goblin'] = ArenaFighter_Goblin
_fighter_kinds['upir'] = ArenaFighter_Vampire
_fighter_kinds['druid'] = ArenaFighter_Druid
_fighter_kinds['saman'] = ArenaFighter_Saman
_fighter_kinds['ledova_kralovna'] = ArenaFighter_IceQueen
_fighter_kinds['kouzelnik'] = ArenaFighter_Wizard
_fighter_kinds['satyr'] = ArenaFighter_Satyr
_fighter_kinds['pasovec'] = ArenaFighter_Pasovec
_fighter_kinds['bansi'] = ArenaFighter_Bansi
_fighter_kinds['naga'] = ArenaFighter_Naga


if __name__ == "__main__":
    pass
