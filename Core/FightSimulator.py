from enum import Enum
from itertools import accumulate
from typing import Callable, Iterator, Union, Optional, List

from Core.Arena import FightArena
import Core.Hero as CHero


class SimulFightResult(Enum):
    LOSE = 1
    DRAW = 2
    WIN = 3

_level_costs_common = dict(zip(range(1,19),[0,10,25,50,150,500,1000,2000,5000,10000,20000,30000,40000,50000,100000,100000,100000,100000]))
_level_costs_rare = dict(zip(range(1,17),[0,50,150,500,1000,2000,5000,10000,20000,30000,40000,50000,100000,100000,100000,100000]))
_level_costs_epic = dict(zip(range(1,15),[0,500,1000,2000,5000,10000,20000,30000,40000,50000,100000,100000,100000,100000]))

_level_costs_cumulative_common = dict(zip(range(1,19),accumulate([0,10,25,50,150,500,1000,2000,5000,10000,20000,30000,40000,50000,100000,100000,100000,100000])))
_level_costs_cumulative_rare = dict(zip(range(1,17),accumulate([0,50,150,500,1000,2000,5000,10000,20000,30000,40000,50000,100000,100000,100000,100000])))
_level_costs_cumulative_epic = dict(zip(range(1,15),accumulate([0,500,1000,2000,5000,10000,20000,30000,40000,50000,100000,100000,100000,100000])))





class HeroFightResult:
    __slots__ = ('hero_data', 'fight_result')

    def __init__(self, hero: CHero.Hero, fight_result: SimulFightResult):
        self.hero_data = hero
        self.fight_result = fight_result

class HeroEnemyCanKillResult:
    __slots__ = ('hero', 'enemies_fight_result')

    def __init__(self, hero: CHero.Hero, enemies_fight_result: [HeroFightResult]):
        self.hero = hero
        self.enemies_fight_result: [HeroFightResult] = enemies_fight_result



class HeroFightScore:
    __slots__ = ('hero_data', 'score', 'order', 'win', 'draw', 'lose',
                 'order_cost_effectivity','upgrade_effectivity', 'score_improvement','level_score_cost_ratio')

    def __init__(self, hero: CHero.Hero, score: int):
        self.hero_data = hero

        self.score = score
        self.win = 0
        self.draw = 0
        self.lose = 0
        self.order = 0
        self.order_cost_effectivity = 0
        self.upgrade_effectivity = 0
        self.score_improvement = 0
        self.level_score_cost_ratio = 0

    def __repr__(self, *args, **kwargs):
        return "{0} score:{1}".format(self.hero_data.name, self.score)

    @staticmethod
    def order_by_score(hero):
        return hero.score

    @staticmethod
    def order_by_level(hero):
        return hero.hero_data.level

    @staticmethod
    def order_by_name(hero):
        return hero.hero_data.name

    @staticmethod
    def order_by_efectivity(hero):
        return hero.order_cost_effectivity

    @staticmethod
    def order_by_score_cost_ratio(hero):
        return hero.level_score_cost_ratio


def simul_fight2(attaker: CHero.Hero, defender: CHero.Hero) -> SimulFightResult:
    tmp_attaker = fighter(attaker, attaker.health)
    tmp_defender = fighter(defender, defender.health)

    if (attaker.attack == 0 and defender.attack == 0): return SimulFightResult.DRAW

    first_reduced_attack = (tmp_attaker.hero.attack * 30) / 100
    index = 0
    while tmp_attaker.health > 0:
        tmp_defender.health = tmp_defender.health - (tmp_attaker.hero.attack - first_reduced_attack)
        first_reduced_attack = 0
        # swap
        tmp_attaker, tmp_defender = tmp_defender, tmp_attaker

    if ((tmp_attaker.hero == attaker and tmp_attaker.health > 0) or \
            (tmp_defender.hero == attaker and tmp_defender.health > 0)): return SimulFightResult.WIN

    return SimulFightResult.LOSE

def simul_fight(attaker: CHero.Hero, defender: CHero.Hero) -> SimulFightResult:

    arena = FightArena()
    arena.set_teams([attaker],[defender])
    arena.run()

    if(not arena.is_team1_win()):
        return SimulFightResult.LOSE
    elif(not arena.is_team2_win()):
        return SimulFightResult.WIN
    else:
        return SimulFightResult.LOSE
    pass


__simul_fight_result_score_lookup= {SimulFightResult.WIN:1, SimulFightResult.DRAW:0, SimulFightResult.LOSE:-1}

def simul_2_fight(attaker: CHero.Hero, defender: CHero.Hero) -> SimulFightResult:
    tmp_score = 0
    fight_status = simul_fight(attaker, defender)
    tmp_score += __simul_fight_result_score_lookup[fight_status]

    fight_status = simul_fight(defender, attaker)
    tmp_score += -__simul_fight_result_score_lookup[fight_status]

    if (tmp_score > 0):
        return  SimulFightResult.WIN
    elif (tmp_score == 0):
        return  SimulFightResult.DRAW
    else:
        return SimulFightResult.LOSE



def simul_fights(heroes_for_evaluate: [CHero.Hero], oponents: [CHero.Hero]) -> [HeroFightScore]:
    result: [HeroFightScore] = []

    for hero in heroes_for_evaluate:
        result_score = 0
        count_win = 0
        count_draw = 0
        count_lose = 0

        for m in range(0, len(oponents)):
            tmp_score = 0
            fight_status = simul_2_fight(hero,oponents[m])

            if (fight_status == SimulFightResult.WIN):
                result_score += 2
                count_win += 1
            elif (fight_status == SimulFightResult.DRAW):
                result_score += 1
                count_draw += 1
            else:
                result_score += 0
                count_lose += 1


        hfs = HeroFightScore(hero, result_score)
        hfs.draw = count_draw
        hfs.lose = count_lose
        hfs.win = count_win

        result.append(hfs)

    return result

def fight_generator(hero_for_evaluate: CHero.Hero, oponents: [CHero.Hero])->Iterator[HeroFightResult]:

    for oponent in oponents:
        fight_status = simul_2_fight(hero_for_evaluate, oponent)

        yield HeroFightResult(oponent,fight_status)

def fight_enemies_can_kill(heroes_for_evaluate: [CHero.Hero], oponents: [CHero.Hero])->[HeroEnemyCanKillResult]:

    result:[HeroEnemyCanKillResult] = []

    for hero in heroes_for_evaluate:
        tmp_dict = {}

        for oponent_result in fight_generator(hero,oponents):
            if(oponent_result.fight_result == SimulFightResult.LOSE): continue

            opo_name = oponent_result.hero_data.name
            if(opo_name not in tmp_dict):
                tmp_dict[opo_name] = oponent_result

            if(tmp_dict[opo_name].hero_data.level < oponent_result.hero_data.level):
                tmp_dict[opo_name] = oponent_result


        tmp_result:[HeroFightResult] = []
        hfr = [c[1] for c in tmp_dict.items()]
        result.append(HeroEnemyCanKillResult(hero,hfr))

    return result

def sfr_fill_order(hfs: [HeroFightScore]):
    hfs.sort(reverse=True, key=lambda x: x.score )

    for x in range(0, len(hfs)):
        hfs[x].order = x

    pass

def sfr_fill_order_effectivity(hfs: [HeroFightScore]):

    x: [HeroFightScore]
    for x in hfs:
        cost = 0
        if(x.hero_data.type == CHero.CONST_Type_Common):
            cost = _level_costs_cumulative_common[x.hero_data.level]
        elif(x.hero_data.type == CHero.CONST_Type_Rare):
            cost = _level_costs_cumulative_rare[x.hero_data.level]
        elif (x.hero_data.type == CHero.CONST_Type_Epic):
            cost = _level_costs_cumulative_epic[x.hero_data.level]

        x.order_cost_effectivity = cost/x.score

    pass

def sfr_fill_score_cost_ratio(hfs: [HeroFightScore]):

    x: [HeroFightScore]
    for x in hfs:
        cost = 0
        if(x.hero_data.type == CHero.CONST_Type_Common):
            cost = _level_costs_cumulative_common[x.hero_data.level]
        elif(x.hero_data.type == CHero.CONST_Type_Rare):
            cost = _level_costs_cumulative_rare[x.hero_data.level]
        elif (x.hero_data.type == CHero.CONST_Type_Epic):
            cost = _level_costs_cumulative_epic[x.hero_data.level]

        x.level_score_cost_ratio = cost/(x.score/x.hero_data.level)

    pass




def sfr_fill_upgrade_effectivity(hfs: [HeroFightScore]):

    x: [HeroFightScore]
    for x in hfs:
        last_level_h = None


        found_level = [_ for _ in hfs if  x.hero_data.name == _.hero_data.name and _.hero_data.level == x.hero_data.level-1]
        if(len(found_level) > 0):
            last_level_h = found_level[0]

        if last_level_h is None: continue

        cost = 0
        if(x.hero_data.type == CHero.CONST_Type_Common):
            cost = _level_costs_common[x.hero_data.level]
        elif(x.hero_data.type == CHero.CONST_Type_Rare):
            cost = _level_costs_rare[x.hero_data.level]
        elif (x.hero_data.type == CHero.CONST_Type_Epic):
            cost = _level_costs_epic[x.hero_data.level]


        x.score_improvement = x.score - last_level_h.score
        if(x.score_improvement != 0):
           x.upgrade_effectivity = cost / x.score_improvement

    pass


class fighter:
    __slots__ = ('hero', 'health')

    def __init__(self, hero: CHero.Hero, health: int):
        self.hero = hero
        self.health = health



"""                -----------------------------------------------------------       ----------- """




if __name__ == "__main__":
    # LoadHeores()
    pass
