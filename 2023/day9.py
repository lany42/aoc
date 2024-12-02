#!/usr/bin/env python


def setup(file="day9.txt"):
    lines = [l.strip() for l in list(open(file))]
    return [[int(i) for i in l.split()] for l in lines]


def reduce_diff(data):
    levels = [data]
    while True:
        levels.append([data[i] - data[i - 1] for i in range(1, len(data))])
        if all([i == 0 for i in levels[-1]]):
            break

        data = levels[-1]

    return levels


def extrapolate(levels):
    levels[-1].append(0)
    for i in reversed(range(0, len(levels) - 1)):
        levels[i].append(levels[i + 1][-1] + levels[i][-1])

    return levels


def extrapolate_left(levels):
    levels[-1].insert(0, 0)
    for i in reversed(range(0, len(levels) - 1)):
        levels[i].insert(0, levels[i][0] - levels[i + 1][0])

    return levels


def part_1():
    data = setup("day9.txt")
    part_1 = 0
    for d in data:
        levels = extrapolate(reduce_diff(d))
        part_1 += levels[0][-1]

    print("Part 1", part_1)


def part_2():
    data = setup("day9.txt")
    part_2 = 0
    for d in data:
        levels = extrapolate_left(reduce_diff(d))
        part_2 += levels[0][0]

    print("Part 2:", part_2)


if __name__ == "__main__":
    part_1()
    part_2()
