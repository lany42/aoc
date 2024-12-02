#!/usr/bin/env python


def get_wins(time, dist):
    wins = 0
    for t in range(0, time + 1):
        rem = time - t
        if t * rem > dist:
            wins += 1

    return wins


def boat_race():
    lines = [l.strip() for l in list(open("day6.txt"))]
    times = [int(s) for s in lines[0].split()[1:]]
    dists = [int(s) for s in lines[1].split()[1:]]

    part_1 = 1
    for t, d in zip(times, dists):
        part_1 *= get_wins(t, d)

    print("Part 1:", part_1)

    p2_time = int("".join([str(x) for x in times]))
    p2_dist = int("".join([str(x) for x in dists]))
    part_2 = get_wins(p2_time, p2_dist)

    print("Part 2:", part_2)


if __name__ == "__main__":
    boat_race()
