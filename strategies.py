from random import random


plays_in_a_game = 10


class Prisoner:
    score = 0
    games_played = 0
    name = 'Abstract'

    @staticmethod
    def strategy(*args, **kwargs):
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

    @staticmethod
    def strategy(*args, **kwargs):
        return True


class PrisonerDefect(Prisoner):
    name = 'Defect'

    @staticmethod
    def strategy(*args, **kwargs):
        return False


class PrisonerCoinFlip(Prisoner):
    name = 'Coin-Flip'

    @staticmethod
    def strategy(*args, **kwargs):
        return random() < 0.5


class PrisonerTitForTat(Prisoner):
    name = 'Tit-for-Tat'

    @staticmethod
    def strategy(*args, **kwargs):
        if kwargs['opponent_history']:
            return kwargs['opponent_history'][-1]
        return True


class PrisonerGrudge(Prisoner):
    name = 'Grudge'

    @staticmethod
    def strategy(*args, **kwargs):
        if kwargs['opponent_history']:
            if False in kwargs['opponent_history']:
                return False
        return True


class PrisonerTitForTwoTat(Prisoner):
    name = 'Tit-for-Two-Tat'

    @staticmethod
    def strategy(*args, **kwargs):
        if kwargs['opponent_history']:
            try:
                if not kwargs['opponent_history'][-1] and not kwargs['opponent_history'][-2]:
                    return False
            except IndexError:
                return True
        return True


class PrisonerBackAndForth(Prisoner):
    name = 'Back-and-Forth'

    @staticmethod
    def strategy(*args, **kwargs):
        if len(kwargs['opponent_history']) % 2:
            return False
        return True


class PrisonerJOSS(Prisoner):
    # Tit-for-Tat but once in a while defect
    name = 'JOSS'

    @staticmethod
    def strategy(*args, **kwargs):
        if kwargs['opponent_history']:
            if random() < 0.15:
                return False
            return kwargs['opponent_history'][-1]
        return True


class PrisonerTitForTatExceptLast(Prisoner):
    # Tit-for-Tat except the very last move: defect
    name = 'Tit-for-Tat-except-last-defect'

    @staticmethod
    def strategy(*args, **kwargs):
        if kwargs['opponent_history']:
            if len(kwargs['opponent_history']) == plays_in_a_game - 1:
                return False
            else:
                return kwargs['opponent_history'][-1]
        return True


class PrisonerTester(Prisoner):
    # This strategy have the ability to identify tit-for-tat or tit-for-two-tat opponent and play so as it can win

    name = "Tester"
    opponent_type = 'Unknown'

    def strategy(self, *args, **kwargs):

        if self.opponent_type == 'Not-nice':
            return PrisonerDefect.strategy(*args, **kwargs)

        op_history = kwargs['opponent_history']
        if op_history and len(op_history) <= 5:

            if len(op_history) == 1 or len(op_history) == 2:
                if not op_history[-1]:
                    self.opponent_type = 'Not-nice'
                return False
            if len(op_history) == 3:
                if op_history[-1]:
                    self.opponent_type = 'Tit-for-Two-Tat'
                else:
                    self.opponent_type = 'Tit-for-Tat'
                return True
            if len(op_history) == 4:
                if op_history[-1]:
                    self.opponent_type = 'CoOp'
                    return False

            if len(op_history) == 5:
                if not op_history[-1]:
                    self.opponent_type = 'Grudge'

        if self.opponent_type == 'Tit-for-Tat':
            return PrisonerTitForTatExceptLast.strategy(*args, **kwargs)
        if self.opponent_type == 'Tit-for-Two-Tat':
            return PrisonerBackAndForth.strategy(*args, **kwargs)
        if self.opponent_type == 'CoOp':
            return PrisonerDefect.strategy(*args, **kwargs)
        if self.opponent_type == 'Grudge':
            return PrisonerDefect.strategy(*args, **kwargs)

        return True
