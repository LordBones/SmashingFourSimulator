from enum import Enum
import  Core.Hero as CHero


class SimulFightResult(Enum):
    LOSE = 1
    DRAW = 2
    WIN = 3


class HeroFightScore:
    __slots__ = ('heroData', 'score')

    def __init__(self, hero: CHero.Hero, score: int):
        self.heroData = hero
        self.score = score

    def __repr__(self,*args, **kwargs):
        return "{0} score:{1}".format(self.heroData.name, self.score)


def simulFight(attaker:CHero.Hero, defender:CHero.Hero)->SimulFightResult:

    pool = (attaker,defender)
    poolLive = [attaker.health, defender.health]

    if(attaker.attack == 0 and defender.attack == 0): return SimulFightResult.DRAW

    index = 0
    while poolLive[index] > 0:
        indexDefender = (index + 1) & 1

        poolLive[indexDefender] = poolLive[indexDefender] - pool[index].attack

        index = (index + 1) & 1

    if(poolLive[0] > 0): return SimulFightResult.WIN

    return SimulFightResult.LOSE


def simulFights(heroes:[CHero.Hero])-> [HeroFightScore]:

    result: [HeroFightScore] = []

    for i in range(0,len(heroes)):
        resultScore = 0

        for m in range(0,len(heroes)):
            fightStatus = simulFight(heroes[i], heroes[m])
            if(fightStatus == SimulFightResult.WIN): resultScore+=2
            elif (fightStatus == SimulFightResult.DRAW): resultScore += 1

            fightStatus = simulFight(heroes[m], heroes[i])
            if (fightStatus == SimulFightResult.LOSE): resultScore += 2
            elif (fightStatus == SimulFightResult.DRAW):  resultScore += 1

        result.append(HeroFightScore(heroes[i],resultScore))

    return result

if __name__ == "__main__":


    #LoadHeores()
    pass