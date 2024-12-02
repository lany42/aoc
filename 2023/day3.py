#!/usr/bin/env python
import re


def boundary(y, x_span):
    s = {(x, y) for x in range(*x_span)}
    return {
        (h, j)
        for x in range(*x_span)
        for h in (x - 1, x, x + 1)
        for j in (y - 1, y, y + 1)
        if (h, j) not in s
    }


def engine_schematic():
    with open("day3.txt") as fd:
        lines = [l.strip() for l in fd.readlines()]

    ROWS = len(lines)
    COLS = len(lines[0])

    symbols = {
        (x, y)
        for y in range(ROWS)
        for x in range(COLS)
        if lines[y][x] not in "1234567890."
    }
    r = re.compile("[0-9]+")

    part_1 = 0
    possible_gears = []
    for y, l in enumerate(lines):
        for m in r.finditer(l):
            bounds = boundary(y, m.span()) & symbols
            if bounds:
                part_1 += int(m.group())
                for h, j in bounds:
                    if lines[j][h] == "*":
                        possible_gears.append((int(m.group()), h, j))

    part_2 = 0
    for idx, g in enumerate(possible_gears):
        p, h, j = g
        for p2, k, l in possible_gears[idx + 1 :]:
            if (h, j) == (k, l):
                part_2 += p * p2
                break

    print("Part 1: ", part_1)
    print("Part 2: ", part_2)


if __name__ == "__main__":
    engine_schematic()
