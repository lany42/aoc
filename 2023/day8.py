#!/usr/bin/env python
import re
import math


def setup(file="day8.txt"):
    lines = [l.strip() for l in list(open(file))]
    r = re.compile("([0-9A-Z]+) = .([0-9A-Z]+), ([0-9A-Z]+).")
    instructions = lines[0]
    nodes = dict()
    for l in lines[2:]:
        m = r.match(l)
        nodes[m.group(1)] = (m.group(2), m.group(3))

    return instructions, nodes


def get_steps(instructions, n, nodes, end_cond):
    steps = 1
    while True:
        for i in instructions:
            if i == "L":
                next = n[0]
            else:
                next = n[1]

            if end_cond(next):
                return steps

            else:
                n = nodes[next]
                steps += 1


def part_1_map():
    instructions, nodes = setup()
    print("Part 1:", get_steps(instructions, nodes["AAA"], nodes, lambda n: n == "ZZZ"))


def part_2_map():
    instructions, nodes = setup("day8.txt")
    ns = [nodes[n] for n in nodes.keys() if n[-1] == "A"]

    # Find the number of steps to the first 'Z' for each starting point
    counts = [get_steps(instructions, n, nodes, lambda n: n[-1] == "Z") for n in ns]

    # Find the least common multiple for the steps
    part_2 = math.lcm(*counts)
    print("Part 2:", part_2)


if __name__ == "__main__":
    part_1_map()
    part_2_map()
