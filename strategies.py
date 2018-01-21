from random import random


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


class PrisonerGrudge(Prisoner):
    name = 'Grudge'

    def strategy(self, *args, **kwargs):
        if kwargs['opponent_history']:
            if False in kwargs['opponent_history']:
                return False
        return True


class PrisonerTitForTwoTat(Prisoner):
    name = 'Tit-for-Two-Tat'

    def strategy(self, *args, **kwargs):
        if kwargs['opponent_history']:
            try:
                if not kwargs['opponent_history'][-1] and not kwargs['opponent_history'][-2]:
                    return False
            except IndexError:
                return True
        return True


class PrisonerBackAndForth(Prisoner):
    name = 'Back-and-Forth'

    def strategy(self, *args, **kwargs):
        if len(kwargs['opponent_history']) % 2:
            return False
        return True


class PrisonerJOSS(Prisoner):
    # Tit-for-Tat but once in a while defect
    name = 'JOSS'

    def strategy(self, *args, **kwargs):
        if kwargs['opponent_history']:
            if random() < 0.15:
                return False
            return kwargs['opponent_history'][-1]
        return True
