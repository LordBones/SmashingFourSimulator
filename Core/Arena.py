
from Core.ArenaFighter import ArenaFighter
from Core.Hero import Hero


class FightArena:
    __slots__ = ('team1', 'team2','arena_teams'
                 )

    def __init__(self ):
        self.team1:[Hero] = []
        self.team2: [Hero] = []

        self.arena_teams:[AFTeam] = []


        pass

    def set_teams(self, team1:[Hero],team2:[Hero]):
        self.team1 = team1
        self.team2 = team2
        pass

    def run(self):

        pass


class AFTeam:
    __slots__ = ('team', 'active_f_index'
                 )

    def __init__(self,fighters: [ArenaFighter]):
        self.team[ArenaFighter] = fighters
        self.active_f_index:int = 0
        pass