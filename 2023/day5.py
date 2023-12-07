#!/usr/bin/env python3.12
import re


def check_ranges(source, ranges):
    for dr, sr in ranges:
        if source in sr:
            return dr[sr.index(source)]

    return source


def is_in(source, ranges):
    for r in ranges:
        if source in r:
            return True

    return False


def reverse_ranges(source, ranges):
    for dr, sr in ranges:
        if source in dr:
            return sr[dr.index(source)]

    return source


def generate_seeds(map_ranges, start=0):
    idx = start
    value = start
    while True:
        for map in reversed(map_ranges):
            value = reverse_ranges(value, map)

        if value is not None:
            yield idx, value

        idx += 1
        value = idx


def almanac():
    lines = [l.strip() for l in list(open("day5.txt"))]
    seeds = [int(s) for s in lines[0].split()[1:]]
    maps = "\n".join(lines[2:]).split("\n\n")

    r = re.compile("([0-9]+) ([0-9]+) ([0-9]+)")
    map_ranges = [list() for _ in range(len(maps))]

    for m, d in zip(maps, map_ranges):
        for match in r.finditer(m):
            dest_s, src_s, length = [int(x) for x in match.group().split()]
            d.append((range(dest_s, dest_s + length), range(src_s, src_s + length)))

    locations = []
    for seed in seeds:
        for map in map_ranges:
            seed = check_ranges(seed, map)

        locations.append(seed)

    part_1 = min(locations)
    print("Part 1:", part_1)


def almanac_2():
    lines = [l.strip() for l in list(open("day5.txt"))]
    seed_ranges = [int(s) for s in lines[0].split()[1:]]
    seed_ranges = [seed_ranges[i : i + 2] for i in range(0, len(seed_ranges), 2)]
    seed_ranges = [range(x, x + y) for x, y in seed_ranges]
    maps = "\n".join(lines[2:]).split("\n\n")

    r = re.compile("([0-9]+) ([0-9]+) ([0-9]+)")
    map_ranges = [list() for _ in range(len(maps))]

    for m, d in zip(maps, map_ranges):
        for match in r.finditer(m):
            dest_s, src_s, length = [int(x) for x in match.group().split()]
            d.append((range(dest_s, dest_s + length), range(src_s, src_s + length)))

    # Start calculating seeds from location 0, compare against seed ranges
    # LOL at seeding the brute force generator with the answer from part 1
    min_loc = 0
    for loc, seed in generate_seeds(map_ranges, 282277027 // 100):
        if is_in(seed, seed_ranges):
            min_loc = loc
            break

    print("Part 2:", min_loc)


if __name__ == "__main__":
    almanac()
    almanac_2()
