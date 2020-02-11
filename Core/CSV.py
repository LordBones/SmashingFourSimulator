from Core import Hero
from Core.FightSimulator import HeroFightScore
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
            attackIncrementPerc = int(row[5])
            healthIncrementPerc = int(row[6])
            attackBonus = int(row[7])
            healthBonus = int(row[8])

            fTypes = {'c': Hero.CONST_Type_Common,
                      'r': Hero.CONST_Type_Rare,
                      'e': Hero.CONST_Type_Epic}
            fTypeParse = fTypes[fType]

            # inicializace bojovnika
            h = Hero.Hero(level, fTypeParse)
            h.attack = attack
            h.name = name
            h.health = health
            h.attackIncrementPerc = attackIncrementPerc
            h.healthIncrementPerc = healthIncrementPerc
            h.attackBonus = attackBonus
            h.healthBonus = healthBonus

            result.append(h)

    csvFile.close()
    return result


def Save_Heroes(fileName: str, heroes:[Hero.Hero]):
    with open(fileName, mode='w', newline='', encoding='utf-8') as file:
        f_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        fTypes_map = { Hero.CONST_Type_Common : 'c',
                   Hero.CONST_Type_Rare : 'r',
                  Hero.CONST_Type_Epic : 'e'}

        f_writer.writerow(['name','type','level', 'attack', 'health', 'attackIncrementPerc', 'healthIncrementPerc', 'attackBonus', 'healthBonus'])
        for hero in heroes:
            f_writer.writerow([
                '{:15}'.format(hero.name) ,
                '{:^3}'.format(fTypes_map[hero.type]),
                '{:>3}'.format(hero.level),
                '{:>5}'.format(hero.attack),
                '{:>5}'.format(hero.health),
                '{:>5}'.format(hero.attackIncrementPerc),
                '{:>5}'.format(hero.healthIncrementPerc),
                '{:>5}'.format(hero.attackBonus),
                '{:>5}'.format(hero.healthBonus)
            ])


def load_HeroeIds(fileName: str) -> [Hero.HeroId]:
    result = []

    with open(fileName, newline='',mode='r') as csvFile:
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

def save_HeroFightScore(fileName: str, heroesScore:[HeroFightScore]):
    with open(fileName, mode='w', newline='', encoding='utf-8') as file:
        f_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        fTypes_map = {Hero.CONST_Type_Common: 'c',
                      Hero.CONST_Type_Rare: 'r',
                      Hero.CONST_Type_Epic: 'e'}

        f_writer.writerow([
            '{:3}'.format('type'),
            '{:20}'.format('name'),
            '{:>3}'.format('level'),
            '{:>3}'.format('attack'),
            '{:>3}'.format('health'),
            '{:>3}'.format('score')])
        for heroScore in heroesScore:
            hero = heroScore.heroData
            f_writer.writerow([
                '{:3}'.format(fTypes_map[hero.type]),
                '{:20}'.format(hero.name) ,
                '{:>3}'.format(hero.level),
                '{:>5}'.format(hero.attack),
                '{:>5}'.format(hero.health),
                '{:>5}'.format(heroScore.score)
            ])


if __name__ == "__main__":
    pass