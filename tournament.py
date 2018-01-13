from random import random
from datetime import datetime


class Prisoner:
    score = 0
    games_played = 0
    history = []
    strategy_f = None

    def strategy(self):
        """
        Based on given information, works on a strategy to make a decision about next move
        :return: True to Co-Operate and False to Defect
        """
        return True

    def play(self):
        move = self.strategy()
        self.history.append(move)
        return move


def strategy_co_op(obj):
    return True


def strategy_defect(obj):
    return False


def strategy_coin_flip(obj):
    return random() < 0.5


class PrisonerCoOp(Prisoner):
    strategy_f = strategy_co_op

    def strategy(self):
        return True


class PrisonerDefect(Prisoner):
    strategy_f = strategy_defect

    def strategy(self):
        return False


class PrisonerCoinFlip(Prisoner):
    strategy_f = strategy_coin_flip

    def strategy(self):
        return random() < 0.5


def play(a_move: bool, b_move: bool) -> (int, int):
    if a_move:
        if b_move:
            return 3, 3
        return 0, 5
    else:
        if b_move:
            return 5, 0
        return 1, 1


# def game(a: Prisoner, b: Prisoner):
#     plays_count = 10
#
#     a.history = []
#     b.history = []
#
#     for i in range(plays_count):
#         a_move = a.strategy()
#         b_move = b.strategy()
#         a.history.append(a_move)
#         b.history.append(b_move)
#         a_score, b_score = play(a_move, b_move)
#         a.score += a_score
#         b.score += b_score
#
#     a.games_played += 1
#     b.games_played += 1


# def game(a: Prisoner, b: Prisoner):
#     plays_count = 10
#
#     a.history = []
#     b.history = []
#
#     a_score_sum = 0
#     b_score_sum = 0
#
#     for i in range(plays_count):
#         a_move = a.strategy()
#         b_move = b.strategy()
#         a.history.append(a_move)
#         b.history.append(b_move)
#         a_score, b_score = play(a_move, b_move)
#         a_score_sum += a_score
#         b_score_sum += b_score
#
#     a.games_played += 1
#     b.games_played += 1


def game(a: Prisoner, b: Prisoner):
    plays_count = 10

    a_history = []
    b_history = []

    a_score_sum = 0
    b_score_sum = 0

    for i in range(plays_count):
        a_move = a.strategy()
        b_move = b.strategy()
        a_history.append(a_move)
        b_history.append(b_move)
        a_score, b_score = play(a_move, b_move)
        a_score_sum += a_score
        b_score_sum += b_score

    a.games_played += 1
    b.games_played += 1


def game2(a: Prisoner, b: Prisoner):
    plays_count = 10

    a_history = []
    b_history = []

    a_score_sum = 0
    b_score_sum = 0

    for i in range(plays_count):
        a_move = a.strategy_f()
        b_move = b.strategy_f()
        a_history.append(a_move)
        b_history.append(b_move)
        a_score, b_score = play(a_move, b_move)
        a_score_sum += a_score
        b_score_sum += b_score

    a.games_played += 1
    b.games_played += 1


class Tournament:
    population = None


print("Hello world!")

benchmark_runs = 100000

bench_start = datetime.now()

for j in range(benchmark_runs):
    a = PrisonerCoinFlip()
    b = PrisonerCoinFlip()
    game(a, b)

print("$$$ " + str(datetime.now() - bench_start))

bench_start = datetime.now()

for k in range(benchmark_runs):
    a = PrisonerCoinFlip()
    b = PrisonerCoinFlip()
    game2(a, b)

print("$$$ " + str(datetime.now() - bench_start))
