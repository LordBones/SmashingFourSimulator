import uuid
import copy
from typing import Optional

CONST_Type_Common = 0
CONST_Type_Rare = 1
CONST_Type_Epic = 2

__max_hero_levels = {CONST_Type_Common: 18, CONST_Type_Rare: 16, CONST_Type_Epic: 14}


class Hero:
    __slots__ = ('id', 'name', 'type', 'level', 'attack', 'health', 'attack_increment_perc', 'health_increment_perc',
                 'ability', 'ability_incr',
                 )

    def __init__(self, level: int, type: int):
        self.id = uuid.uuid4()
        self.name = 'generic'
        self.type = type
        self.level = level
        self.attack = 0
        self.health = 1
        self.attack_increment_perc = 1
        self.health_increment_perc = 1
        self.ability = 1
        self.ability_incr = 0

    def set_name(self, name: str):
        self.name = name

    """def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result"""


class HeroId:
    __slots__ = ('id', 'name', 'level')

    def __init__(self, level: int, name: str):
        self.id = uuid.uuid4()
        self.name = name
        self.level = level


"""
vrati vsechny hrdiny podle heroId
"""


def get_all_heroes_by_hero_id(for_match: [HeroId], heros_src: [Hero]) -> [Hero]:
    result: [Hero] = []

    for hi in for_match:
        match = [_ for _ in heros_src if (_.name == hi.name and _.level == hi.level)]
        if (len(match) > 0):
            result.append(match[0])

    return result


"""
vrati vsechny hrdiny o x level vyssich podle heroId
"""


def get_all_heroes_next_level_by_hero_id(for_match: [HeroId], heros_src: [Hero], level_increment: int, name_suffix:str) -> [Hero]:
    result: [Hero] = []

    for hi in for_match:
        next_level = hi.level + level_increment
        match = [_ for _ in heros_src if (_.name == hi.name and _.level == next_level)]
        if (len(match) > 0):
            new_hero = copy.deepcopy(match[0])
            new_hero.name = new_hero.name+name_suffix
            result.append(new_hero)

    return result

def get_heroes_by_hero_name(hero_name: str, heros_src: [Hero]) -> [Hero]:
    result: [Hero] = []

    for hi in heros_src:
        if (hi.name == hero_name):
            new_hero = copy.deepcopy(hi)
            result.append(new_hero)

    return result


"""
generuje ostatni levely tohoto hrdiny
"""


def get_other_levels_hero(hero_src: Hero, exclude_levels: [int]) -> [Hero]:
    max_level = __max_hero_levels[hero_src.type]

    result: [Hero] = []
    for level in range(1, max_level + 1):
        new_hero = None
        if level not in exclude_levels:
            new_hero = get_other_level_hero(hero_src, level)

        if (new_hero is not None):
            result.append(new_hero)

    return result


def get_other_level_hero(hero_src: Hero, new_level: int) -> Optional[Hero]:
    if (not __check_can_gen_new_hero_level(hero_src, new_level)):
        return None

    new_hero = copy.copy(hero_src)
    new_hero.level = new_level
    new_hero.id = uuid.uuid4()

    if (hero_src.level < new_level):
        count_levels = new_level - hero_src.level
        new_hero.attack = __compute_hero_param_up(hero_src.attack, hero_src.attack_increment_perc, count_levels)
        new_hero.health = __compute_hero_param_up(hero_src.health, hero_src.health_increment_perc, count_levels)
        new_hero.ability = __compute_hero_param_up(hero_src.ability, hero_src.ability_incr, count_levels)
    else:
        count_levels = hero_src.level - new_level
        new_hero.attack = __compute_hero_param_down(hero_src.attack, hero_src.attack_increment_perc, count_levels)
        new_hero.health = __compute_hero_param_down(hero_src.health, hero_src.health_increment_perc, count_levels)
        new_hero.ability = __compute_hero_param_down(hero_src.ability, hero_src.ability_incr, count_levels)

    return new_hero


def __compute_hero_param_down(data: int, data_perc_incr: int, count_levels: int) -> int:
    result = data
    for i in range(1, count_levels + 1):
        result = (result / (data_perc_incr + 100)) * 100

    return int(result)


def __compute_hero_param_up(data: int, data_perc_incr: int, count_levels: int) -> int:
    result = data
    for i in range(1, count_levels + 1):
        result = ((result / 100) * (data_perc_incr + 100))

    return int(result)


def __check_can_gen_new_hero_level(hero_src: Hero, new_level: int) -> bool:
    if (new_level < 1 | new_level > __max_hero_levels[hero_src.type] | new_level == hero_src.level):
        return False

    return True
