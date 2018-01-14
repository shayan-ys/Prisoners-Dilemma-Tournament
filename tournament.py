from random import random
from datetime import datetime


class Prisoner:
    score = 0
    games_played = 0
    history = []
    strategy_f = None

    def strategy(self, *args, **kwargs):
        """
        Based on given information, works on a strategy to make a decision about next move
        :return: True to Co-Operate and False to Defect
        """
        return True

    def play(self, *args, **kwargs):
        move = self.strategy(*args, **kwargs)
        self.history.append(move)
        return move


class PrisonerCoOp(Prisoner):

    def strategy(self, *args, **kwargs):
        return True


class PrisonerDefect(Prisoner):

    def strategy(self, *args, **kwargs):
        return False


class PrisonerCoinFlip(Prisoner):

    def strategy(self, *args, **kwargs):
        return random() < 0.5


# class PrisonerTitForTat(Prisoner):
#
#     def strategy(self, *args, **kwargs):
#         try:
#             return kwargs['opponent_history'][-1]
#         except IndexError:
#             return True


class PrisonerTitForTat(Prisoner):

    def strategy(self, *args, **kwargs):
        if kwargs['opponent_history']:
            return kwargs['opponent_history'][-1]
        return True


# class PrisonerTitForTat2(Prisoner):
#
#     def strategy(self, *args, **kwargs):
#         return kwargs['opponent_history'][-1] if kwargs['opponent_history'] else True


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


# def game(a: Prisoner, b: Prisoner):
#     plays_count = 10
#
#     a_history = []
#     b_history = []
#
#     a_score_sum = 0
#     b_score_sum = 0
#
#     for i in range(plays_count):
#         a_move = a.strategy()
#         b_move = b.strategy()
#         a_history.append(a_move)
#         b_history.append(b_move)
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
        a_move = a.strategy(opponent_history=b_history)
        b_move = b.strategy(opponent_history=a_history)
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

for k in range(benchmark_runs):
    a = PrisonerCoinFlip()
    b = PrisonerTitForTat()
    game(a, b)

print("$$$ " + str(datetime.now() - bench_start))
