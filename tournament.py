from strategies import *
from report import report_to_spreadsheet
from random import shuffle
from datetime import datetime


def play(a_move: bool, b_move: bool) -> (int, int):
    if a_move:
        if b_move:
            return 3, 3
        return 0, 5
    else:
        if b_move:
            return 5, 0
        return 1, 1


def game(a: Prisoner, b: Prisoner):
    a_history = []
    b_history = []

    a_score_sum = 0
    b_score_sum = 0

    for i in range(plays_in_a_game):
        a_move = a.strategy(opponent_history=b_history)
        b_move = b.strategy(opponent_history=a_history)
        a_history.append(a_move)
        b_history.append(b_move)
        a_score, b_score = play(a_move, b_move)
        a_score_sum += a_score
        b_score_sum += b_score
        # print(str(a_move) + ' - ' + str(b_move))

    a.score += a_score_sum
    b.score += b_score_sum
    a.games_played += 1
    b.games_played += 1


class Tournament:
    population = []
    pop_seed = {}
    pop_seed_memory = []
    pop_len = 0
    pop_shuffle_ratio = 0
    evo_members_replacement_count = 10
    evo_games_ratio = 1000

    report_shuffle_count = 0
    report_evo_count = 0

    def __init__(self, *args, **kwargs):
        self.population = []

        if 'evo_games_ratio' in kwargs:
            self.evo_games_ratio = int(kwargs['evo_games_ratio'])

        if 'seed_counts' in kwargs:
            self.seed(kwargs['seed_counts'])

    def seed(self, seed_counts: dict=None):
        if not seed_counts:
            seed_counts = self.pop_seed

        self.pop_seed_memory.append(dict(seed_counts))

        for prisoner_type, count in seed_counts.items():
            for i in range(count):
                self.population.append(prisoner_type())
        self.pop_seed = seed_counts
        self.pop_len = len(self.population)
        if self.pop_len % 2 == 0:
            self.pop_shuffle_ratio = self.pop_len / 2
        else:
            self.pop_shuffle_ratio = self.pop_len
        self.evo_games_ratio = max(1, int(self.evo_games_ratio / self.pop_shuffle_ratio) * self.pop_shuffle_ratio)

    def play_next(self, play_index: int=0):
        if play_index and not play_index % self.pop_shuffle_ratio:
            if not play_index % self.evo_games_ratio:
                self.report_evo_count += 1
                if not self.evolution():
                    return False
            shuffle(self.population)
            self.report_shuffle_count += 1

        player_1 = self.population.pop(0)
        player_2 = self.population.pop(0)

        game(player_1, player_2)

        self.population.append(player_1)
        self.population.append(player_2)

        return True

    def find_extreme_members(self) -> (list, list):
        best_members = []
        worst_members = []

        for indv in self.population:
            indv = indv   # type: Prisoner
            len_best_members = len(best_members)

            if len_best_members == self.evo_members_replacement_count and indv.score > best_members[0].score:
                best_members.pop(0)
                len_best_members -= 1

            if len_best_members < self.evo_members_replacement_count:
                # todo: making the following code a function and add it to previous if will eliminate one 'if'
                insert_point = 0
                add_before = False
                while insert_point < len(best_members):
                    if indv.score < best_members[insert_point].score:
                        add_before = True
                        break
                    insert_point += 1
                if add_before:
                    best_members.insert(insert_point, indv)
                else:
                    best_members.append(indv)

            len_worst_members = len(worst_members)

            if len_worst_members == self.evo_members_replacement_count and indv.score < worst_members[0].score:
                worst_members.pop(0)
                len_worst_members -= 1

            if len_worst_members < self.evo_members_replacement_count:
                # todo: making the following code a function and add it to previous if will eliminate one 'if'
                insert_point = 0
                add_before = False
                while insert_point < len(worst_members):
                    if indv.score > worst_members[insert_point].score:
                        add_before = True
                        break
                    insert_point += 1
                if add_before:
                    worst_members.insert(insert_point, indv)
                else:
                    worst_members.append(indv)

        return best_members, worst_members

    def evolution(self) -> bool:
        # find top for e.g. 3
        # find worst 3
        best_mems, worst_mems = self.find_extreme_members()
        # new members, same types as top 3
        for member in best_mems:
            self.pop_seed[type(member)] += 1
        # deleting members, same as worst 3
        for member in worst_mems:
            self.pop_seed[type(member)] -= 1
        self.population = []
        self.seed()

        # search for dominant
        for prisoner_type, type_count in self.pop_seed.items():
            if type_count == self.pop_len:
                print('"' + prisoner_type.name + '" dominated the population !')
                return False
            elif type_count > 0:
                # even one non-zero type means there is no dominant in population
                break
        return True

    def print_report(self):
        print('--- Report: ---')
        print('Shuffle ratio was: ' + str(self.pop_shuffle_ratio))
        print('Shuffled ' + str(self.report_shuffle_count) + ' times.')
        print('Populated ' + str(self.report_evo_count) + ' times.')
        calculated_report = {
            'Shuffle ratio': self.pop_shuffle_ratio,
            'Shuffled count': self.report_shuffle_count,
            'Populated count': self.report_evo_count
        }
        print('--- Diversity: ---')
        for prisoner_type, type_count in self.pop_seed.items():
            print(prisoner_type.name + ': ' + str(type_count))

        # print('--- Average scores: ---')
        #
        # avg_scores = {}
        # for member in self.population:
        #     try:
        #         avg_scores[type(member)] += member.score
        #     except KeyError:
        #         avg_scores[type(member)] = member.score
        #
        # for avg_member, avg_score in avg_scores.items():
        #     print(str(avg_member) + ': ' + str(avg_score))
        return calculated_report


# game(PrisonerBackAndForth(), PrisonerTitForTatExceptLast())

tour = Tournament(seed_counts={
    PrisonerCoOp: 0,
    PrisonerDefect: 40,
    PrisonerCoinFlip: 0,
    PrisonerBackAndForth: 0,
    PrisonerTitForTat: 40,
    PrisonerTitForTwoTat: 40,
    PrisonerTitForTatExceptLast: 40,
    PrisonerJOSS: 40,
    PrisonerGrudge: 40
})

print(tour.population)
bench_start = datetime.now()
for i in range(100000):
    if not tour.play_next(i):
        break
print("$$$ " + str(datetime.now() - bench_start))
# print(tour.population)
report = tour.print_report()
report['runtime'] = str(datetime.now() - bench_start)
report_to_spreadsheet(tour, **report)
