from enum import Enum
import Core.Hero as CHero


class SimulFightResult(Enum):
    LOSE = 1
    DRAW = 2
    WIN = 3

_level_costs_common = dict(zip(range(1,19),[0,10,25,50,150,500,1000,2000,5000,10000,20000,30000,40000,50000,100000,100000,100000,100000]))
_level_costs_rare = dict(zip(range(1,17),[0,50,150,500,1000,2000,5000,10000,20000,30000,40000,50000,100000,100000,100000,100000]))
_level_costs_epic = dict(zip(range(1,15),[0,500,1000,2000,5000,10000,20000,30000,40000,50000,100000,100000,100000,100000]))


class HeroFightScore:
    __slots__ = ('hero_data', 'score', 'order', 'win', 'draw', 'lose', 'order_cost_effectivity')

    def __init__(self, hero: CHero.Hero, score: int):
        self.hero_data = hero
        self.score = score
        self.win = 0
        self.draw = 0
        self.lose = 0
        self.order = 0
        self.order_cost_effectivity = 0

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


def simul_fight(attaker: CHero.Hero, defender: CHero.Hero) -> SimulFightResult:
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


def simul_fights(heroes_for_evaluate: [CHero.Hero], oponents: [CHero.Hero]) -> [HeroFightScore]:
    result: [HeroFightScore] = []

    for hero in heroes_for_evaluate:
        result_score = 0
        count_win = 0
        count_draw = 0
        count_lose = 0

        for m in range(0, len(oponents)):
            tmp_score = 0
            fight_status = simul_fight(hero, oponents[m])
            if (fight_status == SimulFightResult.WIN):
                tmp_score+=1
            elif (fight_status == SimulFightResult.DRAW):
                tmp_score += 0
            else:
                tmp_score -= 1

            fight_status = simul_fight(oponents[m], hero)
            if (fight_status == SimulFightResult.LOSE):
                tmp_score += 1
            elif (fight_status == SimulFightResult.DRAW):
                tmp_score += 0
            else:
                tmp_score -= 1

            if(tmp_score > 0):
                result_score += 2
                count_win += 1
            elif(tmp_score == 0):
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


def sfr_fill_order(hfs: [HeroFightScore]):
    hfs.sort(reverse=True, key=HeroFightScore.order_by_score)

    for x in range(0, len(hfs)):
        hfs[x].order = x

    pass

def sfr_fill_order_effectivity(hfs: [HeroFightScore]):

    x: [HeroFightScore]
    for x in hfs:
        cost = 0
        if(x.hero_data.type == CHero.CONST_Type_Common):
            cost = _level_costs_common[x.hero_data.level]
        elif(x.hero_data.type == CHero.CONST_Type_Rare):
            cost = _level_costs_rare[x.hero_data.level]
        elif (x.hero_data.type == CHero.CONST_Type_Epic):
            cost = _level_costs_epic[x.hero_data.level]

        x.order_cost_effectivity = cost/x.score

    pass


class fighter:
    __slots__ = ('hero', 'health')

    def __init__(self, hero: CHero.Hero, health: int):
        self.hero = hero
        self.health = health


if __name__ == "__main__":
    # LoadHeores()
    pass
