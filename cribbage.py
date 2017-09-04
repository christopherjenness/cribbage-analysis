import itertools
import pydealer


class CribbageHand(pydealer.stack.Stack):
    """Class for handling cribbage hands"""

    def __init__(self, cards):
        self._cards = list(cards)
        self.assign_card_values()
        self.assign_card_nums()

    def __lt__(self, other):
        return self.score() < other.score()

    def __le__(self, other):
        return self.score() <= other.score()

    def __eq__(self, other):
        return self.score() == other.score()

    def __ne__(self, other):
        return self.score() != other.score()

    def __gt__(self, other):
        return self.score() > other.score()

    def __ge__(self, other):
        return self.score() >= other.score()

    def assign_card_nums(self):
        for card in self._cards:
            if card.value == 'Jack':
                card.num = 11
            elif card.value == 'Queen':
                card.num = 12
            elif card.value == 'King':
                card.num = 13
            elif card.value == 'Ace':
                card.num = 1
            else:
                card.num = int(card.value)

    def assign_card_values(self):
        for card in self._cards:
            if card.value in ['Queen', 'Jack', 'King']:
                card.count_value = 10
            elif card.value == 'Ace':
                card.count_value = 1
            else:
                card.count_value = int(card.value)

    def score(self):
        pairs = self.score_pairs()
        fifteens = self.score_fifteens()
        runs = self.score_runs()
        flush = self.score_flush()
        knobs = self.score_knobs()
        return pairs + fifteens + runs + flush + knobs

    def score_pairs(self):
        nums = [card.num for card in self._cards]
        pairs = len(set([card for card in nums
                    if nums.count(card) == 2]))
        trips = len(set([card for card in nums
                    if nums.count(card) == 3]))
        quads = len(set([card for card in nums
                    if nums.count(card) == 4]))
        pair_score = (pairs * 2) + (trips * 6) + (quads * 12)
        return pair_score

    def score_fifteens(self):
        values = [card.count_value for card in self._cards]
        fifteens = 0
        for i in range(2, 6):
            for seq in itertools.combinations(values, i):
                if sum(seq) == 15:
                    fifteens += 1
        return fifteens * 2

    def score_runs(self):
        values = [card.num for card in self._cards]
        threes, fours = 0, 0
        for i in range(2, 6):
            for seq in itertools.combinations(values, i):
                set_seq = set(seq)
                is_run = ((max(set_seq) - min(set_seq) + 1) == i
                          and len(set_seq) == i)
                if is_run and len(set_seq) == 5:
                    return 5
                if is_run and len(set_seq) == 4:
                    fours += 1
                if is_run and len(set_seq) == 3:
                    threes += 1
        if fours:
            return fours * 4
        return threes * 3

    def score_knobs(self):
        if len(self._cards) == 5:
            test_suits = []
            crib_suit = self._cards[4].suit
            for card in self._cards[:4]:
                if card.value == 'Jack':
                    test_suits.append(card.suit)
            if crib_suit in test_suits:
                return 1
        return 0

    def score_flush(self):
        test_suit = self._cards[3].suit
        for card in self._cards[:3]:
            if card.suit != test_suit:
                return 0
        if len(self._cards) == 5:
            if self._cards[4].suit == test_suit:
                return 5
        return 4
