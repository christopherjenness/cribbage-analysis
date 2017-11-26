import itertools
import pydealer
from cribbage import CribbageHand


def deal_hand():
    deck = pydealer.Deck()
    deck.shuffle()
    hand = deck.deal(7)
    return CribbageHand(cards=hand)


def simulate_hand(strategy):
    initial_hand = deal_hand()
    hand = strategy(initial_hand)
    return hand


def random_strategy(initial_hand):
    """This strategy throws two random cards"""

    saved_cards = initial_hand._cards[2:]
    return CribbageHand(cards=saved_cards)


def best_oracle_strategy(initial_hand):
    """This strategy waits to see what the cut is before throwing
    the two best cards.  Obviously, it is not a possible strategy"""

    best_hand = None
    for cards in itertools.combinations(initial_hand._cards[:6], 4):
        hand = CribbageHand(list(cards) + [initial_hand._cards[6]])
        if not best_hand:
            best_hand = hand
        if hand > best_hand:
            best_hand = hand
    return best_hand


def worst_oracle_strategy(initial_hand):
    """This strategy waits to see what the cut is before throwing
    the  worst cards.  Obviously, it is not a possible strategy"""

    worst_hand = None
    for cards in itertools.combinations(initial_hand._cards[:6], 4):
        hand = CribbageHand(list(cards) + [initial_hand._cards[6]])
        if not worst_hand:
            worst_hand = hand
        if hand < worst_hand:
            worst_hand = hand
    return worst_hand


def best_blind_strategy(initial_hand):
    """This strategy saves the most pre-cut points possible"""
    best_hand = None
    for cards in itertools.combinations(initial_hand._cards[:6], 4):
        hand = CribbageHand(list(cards))
        if not best_hand:
            best_hand = hand
        if hand > best_hand:
            best_hand = hand
    final_hand = CribbageHand(list(best_hand._cards) +
                              [initial_hand._cards[6]])
    return final_hand


def best_blind_strategy_3player(initial_hand):
    """This strategy saves the most pre-cut points possible
    for a 3 player hand"""
    best_hand = None
    for cards in itertools.combinations(initial_hand._cards[:5], 4):
        hand = CribbageHand(list(cards))
        if not best_hand:
            best_hand = hand
        if hand > best_hand:
            best_hand = hand
    final_hand = CribbageHand(list(best_hand._cards) +
                              [initial_hand._cards[6]])
    return final_hand
