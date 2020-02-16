from typing import List

import Core.CSV
import Core.Hero
import cProfile
import gc

import Core.FightSimulator as FSimulator
from Core.FightSimulator import HeroFightScore


def gen_missing_heroes_levels(heroes: [Core.Hero]):
    tmp_result: [Core.Hero] = []
    tmp_heroes: [Core.Hero] = heroes
    while len(tmp_heroes) > 0:
        hero = tmp_heroes[0]

        exclude_levels = list((r.level for r in tmp_heroes if r.name == hero.name))
        exclude_heroes = list((r for r in tmp_heroes if r.name == hero.name))
        tmp_heroes = list((r for r in tmp_heroes if r.name != hero.name))

        newHeroes = Core.Hero.get_other_levels_hero(hero, exclude_levels)


        tmp_result.extend(newHeroes)
        tmp_result.extend(exclude_heroes)

    return tmp_result


def gen_heores_db():
    out = Core.CSV.load_Heroes("InputData/Heroes.csv")

    new_out = gen_missing_heroes_levels(out)
    new_out.sort(reverse=False, key=Core.Hero.Hero.order_by_level)
    new_out.sort(reverse=False, key=Core.Hero.Hero.order_by_name)

    Core.CSV.save_heroes("InputData/HeroesDB.csv", new_out)
    print('dd')


def compute_all_heroes_fight():
    out = Core.CSV.load_Heroes("InputData/HeroesDB.csv")

    hf_score: List[HeroFightScore] = compute_heroes_fight(out)
    save_fight_results(hf_score, 'HeroesAll')
    pass

def compute_onehero_fight(hero_name:str, file_name:str):
    heroes_db = Core.CSV.load_Heroes("InputData/HeroesDB.csv")

    heroes_for_compute = Core.Hero.get_heroes_by_hero_name(hero_name,heroes_db)

    hf_score: List[HeroFightScore] = compute_heroes_fight(heroes_for_compute)
    save_fight_results(hf_score, 'OH_{0}_'.format(file_name))
    pass

def compute_mycards_heroes_fight():
    heroes_db = Core.CSV.load_Heroes("InputData/HeroesDB.csv")
    my_heroes = Core.CSV.load_heroe_ids("InputData/MyHeroesCards.csv")

    heroes_for_compute: [Core.Hero.Hero] = Core.Hero.get_all_heroes_by_hero_id(my_heroes, heroes_db)
    max_level = max(_.level for _ in heroes_for_compute )
    heroes_for_compute_next_levels: [Core.Hero.Hero] = Core.Hero.get_all_heroes_next_level_by_hero_id(my_heroes,heroes_db,1,max_level+1)

    heroes_for_compute.extend(heroes_for_compute_next_levels)

    hf_score: List[HeroFightScore] = compute_heroes_fight(heroes_for_compute)
    save_fight_results(hf_score, 'MyHeroesCards')

    special_prefix = [_ for _ in hf_score if _.hero_data.help_mark is True ]
    special = [_ for _ in hf_score if _.hero_data.help_mark is False]

    special_prefix.sort(reverse=False, key=Core.FightSimulator.HeroFightScore.order_by_score_cost_ratio)
    special_prefix.sort(reverse=True, key=Core.FightSimulator.HeroFightScore.order_by_level)
    special.sort(reverse=False, key=Core.FightSimulator.HeroFightScore.order_by_score_cost_ratio)
    special.sort(reverse=True, key=Core.FightSimulator.HeroFightScore.order_by_level)

    special_prefix.extend(special)

    Core.CSV.save_hero_fight_score("ResultData/{0}_FR_sortUpgrade.csv".format('MyHeroesCards'), special_prefix)
    pass

def compute_heroes_fight(heroes:[Core.Hero.Hero]) -> [Core.FightSimulator.HeroFightScore]:
    heroes_db = Core.CSV.load_Heroes("InputData/HeroesDB.csv")

    result = FSimulator.simul_fights(heroes, heroes_db)
    FSimulator.sfr_fill_order(result)
    FSimulator.sfr_fill_order_effectivity(result)
    FSimulator.sfr_fill_upgrade_effectivity(result)
    FSimulator.sfr_fill_score_cost_ratio(result)

    return result

def save_fight_results(results: [Core.FightSimulator.HeroFightScore], result_name:str):
    results.sort(reverse=True, key=Core.FightSimulator.HeroFightScore.order_by_level)
    results.sort(reverse=True, key=Core.FightSimulator.HeroFightScore.order_by_name)

    Core.CSV.save_hero_fight_score("ResultData/{0}_FR.csv".format(result_name), results)

    results.sort(reverse=True, key=Core.FightSimulator.HeroFightScore.order_by_score)
    Core.CSV.save_hero_fight_score("ResultData/{0}_FR_sortScore.csv".format(result_name), results)
    results.sort(reverse=True, key=Core.FightSimulator.HeroFightScore.order_by_level)
    Core.CSV.save_hero_fight_score("ResultData/{0}_FR_sortLevel.csv".format(result_name), results)

    results.sort(reverse=True, key=Core.FightSimulator.HeroFightScore.order_by_efectivity)
    Core.CSV.save_hero_fight_score("ResultData/{0}_FR_sortEfectivity.csv".format(result_name), results)
    results.sort(reverse=True, key=Core.FightSimulator.HeroFightScore.order_by_score_cost_ratio)
    Core.CSV.save_hero_fight_score("ResultData/{0}_FR_sortCostRatio.csv".format(result_name), results)

    pass


if __name__ == "__main__":
    # cProfile.run('compute_all_heroes_fight()')

    gen_heores_db()
    compute_all_heroes_fight()
    compute_mycards_heroes_fight()
    # compute_onehero_fight('zombie')
    #compute_onehero_fight('zombie','zombieNext')

    #    kk = gc.get_stats()
    #    print(kk)
    pass
