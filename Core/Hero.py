import uuid
import copy

CONST_Type_Common = 0
CONST_Type_Rare = 1
CONST_Type_Epic = 2

__maxHeroLevels = {CONST_Type_Common : 12, CONST_Type_Rare : 10, CONST_Type_Epic : 8}

class Hero:
    __slots__ = ('id','name', 'type', 'level', 'attack', 'health', 'attackIncrementPerc', 'healthIncrementPerc',
                 'attackBonus', 'healthBonus',
                 )

    def __init__(self, level: int, type: int):
        self.id = uuid.uuid4()
        self.name = 'generic'
        self.type = type
        self.level = level
        self.attack = 0
        self.health = 1
        self.attackIncrementPerc = 1
        self.healthIncrementPerc = 1
        self.attackBonus = 1
        self.healthBonus = 0

    """def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result"""


class HeroId:
    __slots__ = ('id','name', 'level'  )

    def __init__(self, level: int, name:str):
        self.id = uuid.uuid4()
        self.name = name
        self.level = level


"""
vrati vsechny hrdiny podle heroId
"""
def get_all_heroes_by_hero_id(for_match:[HeroId],   herosSrc: [Hero])->[Hero]:
    result: [Hero] = []

    for hi in for_match:
        match =  [_ for _ in herosSrc if (_.name == hi.name and _.level == hi.level)]
        if(len(match) > 0):
            result.append(match[0])

    return result

"""
generuje ostatni levely tohoto hrdiny
"""
def getOtherLevelsHero(heroSrc: Hero, excludeLevels:[int])->[Hero]:
    maxLevel = __maxHeroLevels[heroSrc.type]

    result:[Hero] = []
    for level in range(1,maxLevel+1):
        newHero = None
        if level not in excludeLevels:
            newHero = getOtherLevelHero(heroSrc,level)

        if(newHero is not None):
            result.append(newHero)

    return result

def getOtherLevelHero(heroSrc: Hero, newLevel:int)->Hero:

    if(not __checkCanGenNewHeroLevel(heroSrc,newLevel)):
        return None

    newHero = copy.copy(heroSrc)
    newHero.level = newLevel
    newHero.id = uuid.uuid4()

    if(heroSrc.level < newLevel):
        countLevels = newLevel - heroSrc.level
        newHero.attack = __computeHeroParamUp(heroSrc.attack,heroSrc.attackIncrementPerc,countLevels)
        newHero.health = __computeHeroParamUp(heroSrc.health,heroSrc.healthIncrementPerc,countLevels)
    else:
        countLevels =  heroSrc.level - newLevel
        newHero.attack = __computeHeroParamDown(heroSrc.attack, heroSrc.attackIncrementPerc, countLevels)
        newHero.health = __computeHeroParamDown(heroSrc.health, heroSrc.healthIncrementPerc, countLevels)

    return newHero

def __computeHeroParamDown(data:int,  dataPercIncr:int, countLevels:int) -> int:
    result = data
    for i in range(1,countLevels+1):
        result = (result/(dataPercIncr+100))*100

    return int(result)

def __computeHeroParamUp(data:int,  dataPercIncr:int, countLevels:int) -> int:
    result = data
    for i in range(1,countLevels+1):
        result = ((result/100)*(dataPercIncr+100))

    return int(result)


def __checkCanGenNewHeroLevel(heroSrc: Hero, newLevel:int) -> bool:
    if(newLevel < 1 | newLevel > __maxHeroLevels[heroSrc.type] | newLevel == heroSrc.level ):
        return False

    return True
