import Core.CSV
import Core.Hero
import cProfile

import Core.FightSimulator as FSimulator


def genMissingHeroesLevels(heroes:[Core.Hero]):

    tmpResult:[Core.Hero]=[]
    tmpHeroes:[Core.Hero]=heroes
    while len(tmpHeroes) > 0:
        hero = tmpHeroes[0]

        excludeLevels = list((r.level for r in tmpHeroes if r.name == hero.name ))
        tmpHeroes = list((r for r in tmpHeroes if r.name != hero.name))

        tmpResult.append(hero)
        newHeroes = Core.Hero.getOtherLevelsHero(hero,excludeLevels)

        for i in newHeroes:
            tmpResult.append(i)

    return tmpResult



def LoadHeores():
    out = Core.CSV.loadHeroes("InputData/Heroes.csv")

    newOut = genMissingHeroesLevels(out)

    Core.CSV.SaveHeroes("InputData/HeroesDB.csv",newOut)
    print('dd')

def ComputeHeroesFight():
    out = Core.CSV.loadHeroes("InputData/HeroesDB.csv")

    result = FSimulator.simulFights(out)
    Core.CSV.save_HeroFightScore("ResultData/HeroesFightResult.csv", result)

    def sortByScore(e):
        return e.score
    def sortByLevel(e):
        return e.heroData.level

    result.sort(reverse=True, key=sortByScore)
    Core.CSV.save_HeroFightScore( "ResultData/HeroesFightResult_sortScore.csv", result)
    result.sort(reverse=True, key=sortByLevel)
    Core.CSV.save_HeroFightScore("ResultData/HeroesFightResult_sortLevel.csv", result)

    pass



if __name__ == "__main__":
    cProfile.run('ComputeHeroesFight()')

    #LoadHeores()
    ComputeHeroesFight()

    pass