
from Core.ArenaFighter import ArenaFighter,get_arena_fighter
from Core.Hero import Hero


class FightArena:
    __slots__ = ('team1', 'team2','arena_teams'
                 )

    def __init__(self ):
        self.team1:[Hero] = []
        self.team2: [Hero] = []

        self.arena_teams:[AFTeam] = ()


        pass

    def set_teams(self, team1:[Hero],team2:[Hero]):
        self.team1 = team1
        self.team2 = team2
        pass

    def is_team1_win(self):
        return len(self.arena_teams[0].alive) > 0

    def is_team2_win(self):
        return len(self.arena_teams[1].alive) > 0


    def run(self):
        self._init_arena_teams()

        index_team_attaker = 0
        index_team_defender = 1

        attaker_team = self.arena_teams[index_team_attaker]
        defender_team = self.arena_teams[index_team_defender]


        safe_counter = 0
        while(safe_counter < 100):

            self._call_round_start(attaker_team.alive)

            attaker = attaker_team.get_active()
            attaker.active_hero_start()

            target_to_hit:[ArenaFighter] = attaker.choose_targets(defender_team.alive,attaker_team.alive)
            for target in target_to_hit:
                if(target.team_group != attaker.team_group):
                    attaker.hit_enemy(target)
                else:
                    attaker.hit_friendly(target)


            attaker.active_hero_end(defender_team.alive)
            FightArena._call_round_end(attaker_team.alive, defender_team.alive )
            FightArena._call_round_end( defender_team.alive,  attaker_team.alive )

            defender_team.remove_deads()

            if(len(defender_team.alive) <= 0):
                break

            attaker_team, defender_team = defender_team, attaker_team
            #index_team_attaker, index_team_defender = index_team_defender, index_team_attaker
            safe_counter += 1

        pass

    def _call_round_start(self, fighters:[ArenaFighter]):
        for i in fighters:
            i.arena_round_start()
        pass

    @staticmethod
    def _call_round_end(fighters:[ArenaFighter], enemies:[ArenaFighter]):
        for i in fighters:
            i.arena_round_end(enemies)
        pass


    def _init_arena_teams(self):
        #self.arena_teams.clear()

        team1 = [get_arena_fighter(_.name, _)  for _ in self.team1]
        team2 = [get_arena_fighter(_.name, _) for _ in self.team2]

        for af in team1:
            af.team_group = 1
            af.reset()

        for af in team2:
            af.team_group = 0
            af.reset()

        self.arena_teams = (AFTeam(team1),AFTeam(team2))
        #self.arena_teams.append()
        pass




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

    def remove_deads(self):
        if(any((_ for _ in self.alive if _.health <= 0))):
            self.dead.append((_ for _ in self.alive if _.health <= 0))
            #prepsat na inplace remove
            self.alive = [_ for _ in self.alive if _.health > 0]
        pass