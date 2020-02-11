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



def GenHeoresDB():
    out = Core.CSV.load_Heroes("InputData/Heroes.csv")

    newOut = genMissingHeroesLevels(out)

    Core.CSV.Save_Heroes("InputData/HeroesDB.csv",newOut)
    print('dd')

def ComputeAllHeroesFight():
    out = Core.CSV.load_Heroes("InputData/HeroesDB.csv")

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

def ComputeHeroesFight():
    heroesDb = Core.CSV.load_Heroes("InputData/HeroesDB.csv")
    myHeroes = Core.CSV.load_HeroeIds("InputData/MyHeroesCards.csv")

    heroesForCompute = Core.Hero.get_all_heroes_by_hero_id(myHeroes,heroesDb)
    result = FSimulator.simulFights(heroesForCompute ,heroesDb)
    Core.CSV.save_HeroFightScore("ResultData/MyHeroesCardsFightResult.csv", result)

    def sortByScore(e):
        return e.score
    def sortByLevel(e):
        return e.heroData.level

    result.sort(reverse=True, key=sortByScore)
    Core.CSV.save_HeroFightScore( "ResultData/MyHeroesCardsFightResult_sortScore.csv", result)
    result.sort(reverse=True, key=sortByLevel)
    Core.CSV.save_HeroFightScore("ResultData/MyHeroesCardsFightResult_sortLevel.csv", result)

    pass



if __name__ == "__main__":
    #cProfile.run('ComputeHeroesFight()')

    #GenHeoresDB()
    #ComputeAllHeroesFight()
    ComputeHeroesFight()

    pass