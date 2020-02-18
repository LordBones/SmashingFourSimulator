
from Core.ArenaFighter import ArenaFighter,get_arena_fighter
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
        self._init_arena_teams()

        index_team_attaker = 0
        index_team_defender = 1

        while(len(self.arena_teams[index_team_defender].alive)):
            attaker_team = self.arena_teams[index_team_attaker]
            defender_team = self.arena_teams[index_team_defender]

            self._call_round_start(attaker_team.alive)

            attaker = self.arena_teams[index_team_attaker].get_active()
            attaker.active_hero_start()

            target_to_hit = attaker.choose_targets(defender_team.alive,attaker_team.alive)



        pass

    def _call_round_start(self, fighters:[ArenaFighter]):
        for i in fighters:
            i.arena_round_start()
        pass

    def _call_round_end(self, fighters:[ArenaFighter]):
        for i in fighters:
            i.arena_round_end()
        pass


    def _init_arena_teams(self):
        self.arena_teams.clear()

        self.arena_teams.append(AFTeam([(get_arena_fighter(_.name, _)  for _ in self.team1)]))
        self.arena_teams.append(AFTeam([(get_arena_fighter(_.name, _) for _ in self.team2)]))




class AFTeam:
    __slots__ = ('alive', 'active_f_index','dead'
                 )

    def __init__(self,fighters: [ArenaFighter]):
        self.alive:[ArenaFighter] = fighters
        self.dead: [ArenaFighter] = []
        self.active_f_index:int = 0
        pass

    def get_active(self)->ArenaFighter:
        return self.alive[self.active_f_index]