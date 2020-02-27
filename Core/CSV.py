from Core import Hero
from statistics import mean
from Core.FightSimulator import HeroFightScore, HeroEnemyCanKillResult
import csv




def load_Heroes(fileName: str) -> [Hero.Hero]:

    result = []

    with open(fileName, newline='',mode='r') as csvFile:
        spamreader = csv.reader(csvFile, delimiter=',', quotechar='"')
        spamreader.__next__()
        for row in spamreader:
            if len(row) == 0 : continue

            name = row[0].strip()
            fType =  row[1].lower().strip()
            level = int(row[2])
            attack = int(row[3])
            health = int(row[4])
            attackIncrPerc = int(row[5])
            healthIncrPerc = int(row[6])
            ability = int(row[7])
            ability_incr = int(row[8])

            fTypes = {'c': Hero.CONST_Type_Common,
                      'r': Hero.CONST_Type_Rare,
                      'e': Hero.CONST_Type_Epic}
            fTypeParse = fTypes[fType]

            # inicializace bojovnika
            h = Hero.Hero(level, fTypeParse)
            h.attack = attack
            h.name = name
            h.health = health
            h.attack_increment_perc = attackIncrPerc
            h.health_increment_perc = healthIncrPerc
            h.ability = ability
            h.ability_incr = ability_incr

            result.append(h)

    csvFile.close()
    return result


def save_heroes(file_name: str, heroes:[Hero.Hero]):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        f_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        f_types_map = { Hero.CONST_Type_Common : 'c',
                   Hero.CONST_Type_Rare : 'r',
                  Hero.CONST_Type_Epic : 'e'}

        f_writer.writerow(['name','type','level', 'attack', 'health', 'attackIncrPerc', 'healthIncrPerc', 'ability', 'abilityIncr'])
        for hero in heroes:
            f_writer.writerow([
                '{:15}'.format(hero.name),
                '{:^3}'.format(f_types_map[hero.type]),
                '{:>3}'.format(hero.level),
                '{:>5}'.format(hero.attack),
                '{:>5}'.format(hero.health),
                '{:>5}'.format(hero.attack_increment_perc),
                '{:>5}'.format(hero.health_increment_perc),
                '{:>5}'.format(hero.ability),
                '{:>5}'.format(hero.ability_incr)
            ])


def load_heroe_ids(file_name: str) -> [Hero.HeroId]:
    result = []

    with open(file_name, newline='', mode='r') as csvFile:
        spamreader = csv.reader(csvFile, delimiter=',', quotechar='"')
        spamreader.__next__()
        for row in spamreader:
            if len(row) == 0 : continue

            name = row[0].strip()
            level = int(row[1])

            # inicializace bojovnika
            h = Hero.HeroId(level, name)

            result.append(h)

    csvFile.close()
    return result

def save_hero_fight_score(file_name: str, heroes_score:[HeroFightScore]):
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        f_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        fTypes_map = {Hero.CONST_Type_Common: 'c',
                      Hero.CONST_Type_Rare: 'r',
                      Hero.CONST_Type_Epic: 'e'}

        f_writer.writerow([
            '{:4}'.format('type'),
            '{:20}'.format('name'),
            '{:>5}'.format('level'),
            '{:>5}'.format('order'),
            '{:>5}'.format('score'),
            '{:>10}'.format('r/s/c'),
            '{:>8}'.format('scoreUp'),
            '{:>12}'.format('efectivity'),
            '{:>12}'.format('efectivityUp'),

            '{:>5}'.format('win'),
            '{:>5}'.format('draw'),
            '{:>5}'.format('lose'),

            '{:>5}'.format('attack'),
            '{:>5}'.format('health')

        ])
        for heroScore in heroes_score:
            hero = heroScore.hero_data
            hero_name = hero.name
            if hero.help_mark:
                hero_name = '* ' + hero_name

            f_writer.writerow([
                '{:4}'.format(fTypes_map[hero.type]),
                '{:20}'.format(hero_name) ,
                '{:>5}'.format(hero.level),
                '{:>5}'.format(heroScore.order),
                '{:>5}'.format(heroScore.score),
                '{:>10}'.format(round(heroScore.level_score_cost_ratio,2)),

                '{:>8}'.format(heroScore.score_improvement),

                '{:>12}'.format(round(heroScore.order_cost_effectivity,2)),
                '{:>12}'.format(round(heroScore.upgrade_effectivity, 2)),

                '{:>5}'.format(heroScore.win),
                '{:>5}'.format(heroScore.draw),
                '{:>5}'.format(heroScore.lose),
                '{:>5}'.format(hero.attack),
                '{:>5}'.format(hero.health),
            ])

def save_who_i_can_kill(file_name: str, heroes_cankill:[HeroEnemyCanKillResult]):



    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        f_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        fTypes_map = {Hero.CONST_Type_Common: 'c',
                      Hero.CONST_Type_Rare: 'r',
                      Hero.CONST_Type_Epic: 'e'}
        count_cols = len(heroes_cankill)

        def get_avg_level(heroes_cankill:[HeroEnemyCanKillResult], type_heroe:int)->[float]:
            tmp = [[_.hero_data.level for _ in x.enemies_fight_result if
                 _.hero_data.type == type_heroe] for x in heroes_cankill]
            for i in range(0,len(tmp)):
                if(len(tmp[i]) == 0):
                    tmp[i].append(-1)

            return [float(mean(_)) for _ in tmp]


        avg_levels_c = get_avg_level(heroes_cankill, Hero.CONST_Type_Common)
        #[float(mean(_.hero_data.level for _ in x.enemies_fight_result if _.hero_data.type == Hero.CONST_Type_Common)) for x in heroes_cankill]
        avg_levels_r = get_avg_level(heroes_cankill, Hero.CONST_Type_Rare)
        avg_levels_e = get_avg_level(heroes_cankill, Hero.CONST_Type_Epic)
       # [
        #    float(mean(_.hero_data.level for _ in x.enemies_fight_result if _.hero_data.type == Hero.CONST_Type_Rare))
        #    for x in heroes_cankill]
        #avg_levels_e = [
        #    float(mean(_.hero_data.level for _ in x.enemies_fight_result if _.hero_data.type == Hero.CONST_Type_Epic))
        #    for x in heroes_cankill]

        header = ['{:20}'.format(fTypes_map[x.hero.type]+ " " + x.hero.name + " " + str(x.hero.level)) for x in heroes_cankill]

        f_writer.writerow(header)
        f_writer.writerow(['{:>20}'.format('{:3.2f}'.format(_)+" avg. lvl c") for _ in avg_levels_c])
        f_writer.writerow(['{:>20}'.format('{:3.2f}'.format(_) + " avg. lvl r") for _ in avg_levels_r])
        f_writer.writerow(['{:>20}'.format('{:3.2f}'.format(_) + " avg. lvl e") for _ in avg_levels_e])

        f_writer.writerow([])
        tmp_enemies = [ x.enemies_fight_result  for x in heroes_cankill]
        for item in tmp_enemies:
            item.sort(reverse=False, key=lambda x:x.hero_data.name)
            item.sort(reverse=False, key=lambda x:x.hero_data.type)

        max_iteration = len(max(tmp_enemies,key= lambda x:len(x)))

        for index in range(0,max_iteration):
            row = []
            for enemies in tmp_enemies:

                text = ""
                if(len(enemies) > index):
                    enemy = enemies[index]
                    text = '{:20}'.format(fTypes_map[enemy.hero_data.type]+" "+ enemy.hero_data.name+ " " + str(enemy.hero_data.level))

                row.append(text)

            f_writer.writerow(row)
    pass



if __name__ == "__main__":
    pass