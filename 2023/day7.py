#!/usr/bin/env python3.12
from enum import Enum, IntEnum, auto

card_map = {
    c: p for c, p in zip("23456789TJQKA", list(range(1, len("23456789TJQKA") + 1)))
}

with_joker = {
    c: p for c, p in zip("J23456789TQKA", list(range(1, len("J23456789TQKA") + 1)))
}


class HandTypes(IntEnum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()

    def __str__(self):
        return Enum.__str__(self)


class Hand:
    def __init__(self, h, use_jokers=False) -> None:
        self._orig_hand = h[0]
        self._hand = h[0]
        self._bid = int(h[1])
        self._use_jokers = use_jokers

        self._score = self._score_hand()

        if not use_jokers:
            self._kickers = [card_map[c] for c in self._orig_hand]

        else:
            self._kickers = [with_joker[c] for c in self._orig_hand]

    def _score_hand(self):
        amounts = [self._hand.count(c) for c in set(self._hand)]
        if 5 in amounts:
            return HandTypes.FIVE_OF_A_KIND

        # Convert jokers to the next card type with the largest amount
        if self._use_jokers and "J" in self._hand:
            not_j = {self._hand.count(c): c for c in set(self._hand) if c != "J"}
            card = not_j[max(not_j.keys())]
            self._hand = self._hand.replace("J", card)
            amounts = [self._hand.count(c) for c in set(self._hand)]

        if 5 in amounts:
            return HandTypes.FIVE_OF_A_KIND

        if 4 in amounts:
            return HandTypes.FOUR_OF_A_KIND

        elif 3 in amounts and 2 in amounts:
            return HandTypes.FULL_HOUSE

        elif 3 in amounts:
            return HandTypes.THREE_OF_A_KIND

        elif amounts.count(2) == 2:
            return HandTypes.TWO_PAIR

        elif 2 in amounts:
            return HandTypes.ONE_PAIR

        else:
            return HandTypes.HIGH_CARD

    def __lt__(self, rhs):
        if self.score != rhs.score:
            return self._score < rhs.score

        else:
            for a, b in zip(self.kickers, rhs.kickers):
                if a != b:
                    return a < b

    @property
    def hand(self):
        return self._hand

    @property
    def bid(self):
        return self._bid

    @property
    def score(self):
        return self._score

    @property
    def kickers(self):
        return self._kickers

    def __str__(self):
        return "{} : {} : {} : {}".format(
            self._orig_hand, self._hand, self._bid, str(self._score)
        )


def camel_cards():
    lines = [l.strip() for l in list(open("day7.txt"))]
    hands = [Hand(tuple(l.split())) for l in lines]

    hands.sort()

    part_1 = 0
    for rank, hand in enumerate(hands):
        part_1 += hand.bid * (rank + 1)

    print("Part 1:", part_1)

    hands2 = [Hand(tuple(l.split()), use_jokers=True) for l in lines]
    hands2.sort()
    part_2 = 0
    for rank, hand in enumerate(hands2):
        part_2 += hand.bid * (rank + 1)

    print("Part 2:", part_2)


if __name__ == "__main__":
    camel_cards()
