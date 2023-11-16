#!/usr/bin/env python3.12
import re


def count_cards(keys, d):
    count = len(keys)
    for k in keys:
        count += count_cards(d[k], d)

    return count


def play_cards():
    lines = [l.strip() for l in list(open("day4.txt"))]
    r = re.compile("[0-9]+")
    cards = dict()

    for l in lines:
        c, ns = l.split(":")
        w = {n.group() for n in r.finditer(ns.split("|")[0])}
        h = {n.group() for n in r.finditer(ns.split("|")[1])}

        cn = int(r.search(c).group())
        cards[cn] = (w, h)

    part_1 = 0
    part_2 = dict()
    part_2_dp = {c: 1 for c in cards}

    for k, v in cards.items():
        w, h = v
        if w & h:
            n_wins = len(w & h)
            part_1 += 2 ** (n_wins - 1)
            part_2[k] = [n for n in range(k + 1, k + n_wins + 1) if n in cards]

            for c in part_2[k]:
                part_2_dp[c] += part_2_dp[k]

        else:
            part_2[k] = []

    # part_2_sol = count_cards(part_2.keys(), part_2)
    print("Part 1: ", part_1)
    # print("Part 2: ", part_2_sol)
    print("Part 2: ", sum(part_2_dp.values()))


if __name__ == "__main__":
    play_cards()
