from random import random, shuffle


class Prisoner:
    score = 0
    games_played = 0
    name = 'Abstract'

    def strategy(self, *args, **kwargs):
        """
        Based on given information, works on a strategy to make a decision about next move
        :return: True to Co-Operate and False to Defect
        """
        return True

    # def play(self, *args, **kwargs):
    #     move = self.strategy(*args, **kwargs)
    #     self.history.append(move)
    #     return move

    def __str__(self):
        if self.games_played:
            return self.name + ' (' + str(int(self.score / self.games_played * 100)) + ' { ' + str(
                self.score) + '/' + str(self.games_played) + ' })'
        else:
            return self.name + ' (newbie)'

    def __repr__(self):
        return self.__str__()


class PrisonerCoOp(Prisoner):
    name = 'Co-Operate'

    def strategy(self, *args, **kwargs):
        return True


class PrisonerDefect(Prisoner):
    name = 'Defect'

    def strategy(self, *args, **kwargs):
        return False


class PrisonerCoinFlip(Prisoner):
    name = 'Coin-Flip'

    def strategy(self, *args, **kwargs):
        return random() < 0.5


class PrisonerTitForTat(Prisoner):
    name = 'Tit-for-Tat'

    def strategy(self, *args, **kwargs):
        if kwargs['opponent_history']:
            return kwargs['opponent_history'][-1]
        return True


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
    plays_count = 10

    a_history = []
    b_history = []

    a_score_sum = 0
    b_score_sum = 0

    for i in range(plays_count):
        a_move = a.strategy(opponent_history=b_history)
        b_move = b.strategy(opponent_history=a_history)
        a_history.append(a_move)
        b_history.append(b_move)
        a_score, b_score = play(a_move, b_move)
        a_score_sum += a_score
        b_score_sum += b_score

    a.score += a_score_sum
    b.score += b_score_sum
    a.games_played += 1
    b.games_played += 1


class Tournament:
    population = []
    pop_len = 0
    evo_members_replacement_count = 3
    evo_games_ratio = 0

    def __init__(self, *args, **kwargs):
        self.population = []

        if 'seed_counts' in kwargs:
            self.seed(kwargs['seed_counts'])

    def seed(self, seed_counts: dict):
        for prisoner_type, count in seed_counts.items():
            for i in range(count):
                self.population.append(prisoner_type())
        self.pop_len = len(self.population)

    def play_next(self, play_index: int=0):
        if play_index and not play_index % self.pop_len:
            shuffle(self.population)

        player_1 = self.population.pop(0)
        player_2 = self.population.pop(0)

        game(player_1, player_2)

        self.population.append(player_1)
        self.population.append(player_2)

    def find_extreme_members(self, given_arr):
        best_members = []
        worst_members = []

        for indv in given_arr:
            len_best_members = len(best_members)

            if len_best_members == self.evo_members_replacement_count and indv > best_members[0]:
                best_members.pop(0)
                len_best_members -= 1

            if len_best_members < self.evo_members_replacement_count:
                # todo: making the following code a function and add it to previous if will eliminate one 'if'
                insert_point = 0
                add_before = False
                while insert_point < len(best_members):
                    if indv < best_members[insert_point]:
                        add_before = True
                        break
                    insert_point += 1
                if add_before:
                    best_members.insert(insert_point, indv)
                else:
                    best_members.append(indv)

            len_worst_members = len(worst_members)

            if len_worst_members == self.evo_members_replacement_count and indv < worst_members[0]:
                worst_members.pop(0)
                len_worst_members -= 1

            if len_worst_members < self.evo_members_replacement_count:
                # todo: making the following code a function and add it to previous if will eliminate one 'if'
                insert_point = 0
                add_before = False
                while insert_point < len(worst_members):
                    if indv > worst_members[insert_point]:
                        add_before = True
                        break
                    insert_point += 1
                if add_before:
                    worst_members.insert(insert_point, indv)
                else:
                    worst_members.append(indv)

            print(indv)
            print(worst_members)
            print(best_members)

    def evolution(self):
        # find top for e.g. 3
        # find worst 3
        # new members, same types as top 3
        pass


print("Hello world!")

pop_seed_counts = {
    PrisonerCoOp: 1,
    PrisonerDefect: 1,
    PrisonerCoinFlip: 1,
    PrisonerTitForTat: 2
}

# benchmark_runs = 100000
#
# bench_start = datetime.now()
#
# for k in range(benchmark_runs):
#     a = PrisonerCoinFlip()
#     b = PrisonerTitForTat()
#     game(a, b)
#
# print("$$$ " + str(datetime.now() - bench_start))

tour = Tournament()
tour.seed(pop_seed_counts)

tour.find_extreme_members([6, 2, 4, 7, 9, 3, 11, 8])

print(tour.population)
for i in range(10):
    tour.play_next(i)
print(tour.population)
