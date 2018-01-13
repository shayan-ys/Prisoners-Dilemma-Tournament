from random import random
from datetime import datetime


rules = {
    'scores_table': (
        ((1, 1), (5, 0)),
        ((0, 5), (3, 3))
    ),
    'scores_table_alt': {
        False: {False: (1, 1), True: (5, 0)},
        True: {False: (0, 5), True: (3, 3)}
    }
}


class Prisoner:
    coins = 0
    games_played = 0
    history = []

    def strategy(self):
        """
        Based on given information, works on a strategy to make a decision about next move
        :return: True to Co-Operate and False to Defect
        """
        pass


class PrisonerCoOp(Prisoner):

    def strategy(self):
        return True


class PrisonerDefect(Prisoner):

    def strategy(self):
        return False


class PrisonerCoinFlip(Prisoner):

    def strategy(self):
        return random() < 0.5


# def play(a_move: bool, b_move: bool) -> (int, int):
#     return rules['scores_table'][int(a_move)][int(b_move)]


def play2(a_move: bool, b_move: bool) -> (int, int):
    return rules['scores_table_alt'][a_move][b_move]


cache = rules['scores_table_alt']


def play_cached(a_move: bool, b_move: bool) -> (int, int):
    return cache[a_move][b_move]


def play_embed(a_move: bool, b_move: bool) -> (int, int):
    return {
        False: {False: (1, 1), True: (5, 0)},
        True: {False: (0, 5), True: (3, 3)}
    }[a_move][b_move]


def play_if(a_move: bool, b_move: bool) -> (int, int):
    if a_move:
        if b_move:
            return 3, 3
        else:
            return 0, 5
    else:
        if b_move:
            return 5, 0
        else:
            return 1, 1


def play_if_2(a_move: bool, b_move: bool) -> (int, int):
    if a_move:
        if b_move:
            return 3, 3
        return 0, 5
    else:
        if b_move:
            return 5, 0
        return 1, 1


def play_if_3(a_move: bool, b_move: bool) -> (int, int):
    if a_move and b_move:
        return 3, 3
    elif a_move and not b_move:
        return 0, 5
    elif not a_move and b_move:
        return 5, 0
    return 1, 1


def game(a: Prisoner, b: Prisoner):
    plays_count = 10

    a.history = []
    b.history = []

    for i in range(plays_count):
        a_move = a.strategy()
        b_move = b.strategy()


class Tournament:
    population = None


print("Hello world!")

# a_score, b_score = play(False, True)
# print(a_score)
# print(b_score)

benchmark_runs = 1000000

bench_start = datetime.now()

for l in range(benchmark_runs):
    a_move = random() < 0.5
    b_move = random() < 0.5
    a_score, b_score = play_if(a_move, b_move)

print("$$$ " + str(datetime.now() - bench_start))
bench_start = datetime.now()

for l in range(benchmark_runs):
    a_move = random() < 0.5
    b_move = random() < 0.5
    a_score, b_score = play_if_2(a_move, b_move)

print("$$$ " + str(datetime.now() - bench_start))
bench_start = datetime.now()

for l in range(benchmark_runs):
    a_move = random() < 0.5
    b_move = random() < 0.5
    a_score, b_score = play_if_3(a_move, b_move)

print("$$$ " + str(datetime.now() - bench_start))
bench_start = datetime.now()
for i in range(benchmark_runs):
    a_move = random() < 0.5
    b_move = random() < 0.5
    a_score, b_score = play2(a_move, b_move)
    # with cast bool to int and check in table of tuples

print("$$$ " + str(datetime.now() - bench_start))
bench_start = datetime.now()

for j in range(benchmark_runs):
    a_move = random() < 0.5
    b_move = random() < 0.5
    a_score, b_score = play_cached(a_move, b_move)

print("$$$ " + str(datetime.now() - bench_start))
# bench_start = datetime.now()
#
# for k in range(benchmark_runs):
#     a_move = random() < 0.5
#     b_move = random() < 0.5
#     a_score, b_score = play_embed(a_move, b_move)
#
# print("$$$ " + str(datetime.now() - bench_start))
