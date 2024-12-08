#!/usr/bin/env python

import re
from itertools import combinations
from multiprocessing import Pool
from pathlib import Path


class Day1:
    def __init__(self, fd) -> None:
        self.list_1 = []
        self.list_2 = []

        for pair in Path(fd).read_text().strip().split("\n"):
            left, right = pair.split()
            self.list_1.append(int(left))
            self.list_2.append(int(right))

        self.list_1.sort()
        self.list_2.sort()

    def part_1(self):
        total_distance = 0
        for left, right in zip(self.list_1, self.list_2):
            total_distance += abs(left - right)

        print(f"Day 01 Part 1: {total_distance}")

        return self

    def part_2(self):
        right_counts = {i: self.list_2.count(i) for i in self.list_2}

        score = 0
        for left in self.list_1:
            score += left * right_counts.get(left, 0)

        print(f"Day 01 Part 2: {score}\n")

        return self


class Day2:
    def __init__(self, fd) -> None:
        self.reports = [
            list(map(int, report.split()))
            for report in Path(fd).read_text().strip().split("\n")
        ]

        self._part_1_safe = 0
        self._part_1_failed_reports = []

    def part_1(self):
        for report in self.reports:
            diffs = [report[i] - b for i, b in enumerate(report[1:])]
            diff_check = all([abs(d) <= 3 for d in diffs])
            rate_check = all([i < 0 for i in diffs]) or all([i > 0 for i in diffs])

            if diff_check and rate_check:
                self._part_1_safe += 1

            else:
                self._part_1_failed_reports.append(report)

        print(f"Day 02 Part 1: {self._part_1_safe}")
        return self

    # Dirty brute force
    def part_2(self):
        n_safe = 0
        for bad_report in self._part_1_failed_reports:
            for i in range(len(bad_report)):
                to_try = bad_report[:]
                to_try.pop(i)

                diffs = [to_try[i] - b for i, b in enumerate(to_try[1:])]
                diff_check = all([abs(d) <= 3 for d in diffs])
                rate_check = all([i < 0 for i in diffs]) or all([i > 0 for i in diffs])

                if diff_check and rate_check:
                    n_safe += 1
                    break

        print(f"Day 02 Part 2: {self._part_1_safe + n_safe}\n")
        return self


class Day3:
    def __init__(self, fd) -> None:
        self._prog = Path(fd).read_text().strip()

    def part_1(self):
        r = re.compile(r"mul\(([0-9]+),([0-9]+)\)")

        total = 0
        for match in r.finditer(self._prog):
            total += int(match.group(1)) * int(match.group(2))

        print(f"Day 03 Part 1: {total}")
        return self

    def part_2(self):
        r = re.compile(r"mul\(([0-9]+),([0-9]+)\)")
        total = 0

        split_donts = self._prog.split("don't()")
        do_lines = [split_donts[0]]

        # Gather all 'do' strs from the split don'ts
        for d in split_donts[1:]:
            do_lines.extend(d.split("do()")[1:])

        # Run the same regex on the new string
        for match in r.finditer("".join(do_lines)):
            total += int(match.group(1)) * int(match.group(2))

        print(f"Day 03 Part 2: {total}\n")
        return self


class Day4:
    def __init__(self, fd) -> None:
        lines = Path(fd).read_text().strip().split("\n")

        self.nrows = len(lines)
        self.ncols = len(lines[0])

        # Gather locations of X, M, A, and S
        symbols = {
            (x, y)
            for y in range(self.nrows)
            for x in range(self.ncols)
            if lines[y][x] in "XMAS"
        }

        # Transform so that they are mapped by X, M, A, and S
        self.xmas = {
            "X": set(),
            "M": set(),
            "A": set(),
            "S": set(),
        }

        for x, y in symbols:
            self.xmas[lines[y][x]].add((x, y))

    # Calculate all possible .MAS grid points given a start (x, y) of the X
    def possible_xmas(self, x, y):
        return [
            [(x + h, y) for h in range(1, 4)],  # Right
            [(x - h, y) for h in range(1, 4)],  # Left
            [(x, y + j) for j in range(1, 4)],  # Up
            [(x, y - j) for j in range(1, 4)],  # Down
            [(x - i, y + i) for i in range(1, 4)],  # UL
            [(x + i, y + i) for i in range(1, 4)],  # UR,
            [(x - i, y - i) for i in range(1, 4)],  # LL,
            [(x + i, y - i) for i in range(1, 4)],  # LR
        ]

    # Calculate all possible positions of the X-MAS given an (x, y) of an A
    # NOTE: Unlike part 1, two possible sequences of 'MAS' must validate
    #       and each 'A' can only have one set
    def possible_x_mas(self, x, y):
        return [
            [
                (x - 1, y + 1),
                (x - 1, y - 1),
                (x + 1, y + 1),
                (x + 1, y - 1),
            ],  # M's Left, S's Right
            [
                (x - 1, y + 1),
                (x + 1, y + 1),
                (x - 1, y - 1),
                (x + 1, y - 1),
            ],  # M's Up, S's Down
            [
                (x + 1, y + 1),
                (x + 1, y - 1),
                (x - 1, y + 1),
                (x - 1, y - 1),
            ],  # M's Right, S's Left
            [
                (x - 1, y - 1),
                (x + 1, y - 1),
                (x - 1, y + 1),
                (x + 1, y + 1),
            ],  # M's Down, S's Up
        ]

    def soln(self):
        # To solve part 1, iterate through all 'X' locations
        # Calculate potential .MAS grid
        # Check if grid points exist in M, A, and S sets
        total_xmas = 0
        for X in self.xmas["X"]:
            for pM, pA, pS in self.possible_xmas(*X):
                if (
                    pM in self.xmas["M"]
                    and pA in self.xmas["A"]
                    and pS in self.xmas["S"]
                ):
                    total_xmas += 1

        print(f"Day 04 Part 1: {total_xmas}")

        # Part 2 is similar, check for a valid sequence of X-MAS
        # by iterating through all 'A's
        total_x_mas = 0
        for A in self.xmas["A"]:
            for m1, m2, s1, s2 in self.possible_x_mas(*A):
                if (
                    m1 in self.xmas["M"]
                    and m2 in self.xmas["M"]
                    and s1 in self.xmas["S"]
                    and s2 in self.xmas["S"]
                ):
                    total_x_mas += 1
                    break

        print(f"Day 04 Part 2: {total_x_mas}\n")


class Day5:
    def __init__(self, fd) -> None:
        text = Path(fd).read_text().strip().split("\n")
        self.before_rules = {}
        self.after_rules = {}
        self.updates = []

        for line in text:
            if "|" in line:
                before, after = tuple(map(int, line.split("|")))
                if before not in self.before_rules:
                    self.before_rules[before] = set()

                if after not in self.after_rules:
                    self.after_rules[after] = set()

                self.before_rules[before].add(after)
                self.after_rules[after].add(before)

            elif "," in line:
                self.updates.append(list(map(int, line.split(","))))

    # Swap a and b within list update
    def _swap(self, a, b, update):
        ia = update.index(a)
        ib = update.index(b)
        update[ia] = b
        update[ib] = a

        return update

    def _checker(self, value, slice, ruleset):
        if value not in ruleset:
            return True, 0

        # All pages in the slice must be in the ruleset for this value
        for v in slice:
            if v not in ruleset[value]:
                return False, v

        return True, 0

    def _check_before(self, value, right):
        return self._checker(value, right, self.before_rules)

    def _check_after(self, value, left):
        return self._checker(value, left, self.after_rules)

    # For part 1, we can validate each page number against the ruleset
    # Any failed checks invalidate the entire update
    def _check_update(self, update):
        for i, value in enumerate(update):
            left = update[:i]
            right = update[i + 1 :]

            rc, _ = self._check_before(value, right)
            if not rc:
                return False

            rc, _ = self._check_after(value, left)
            if not rc:
                return False

        return True

    # Part 2, order the failed update based on the ruleset
    # Check for failed before and after checks, then simply swap those
    # two values and restart the checks (aka bubble-sort)
    def _check_and_swap(self, update):
        for i, value in enumerate(update):
            left = update[:i]
            right = update[i + 1 :]

            rc, v = self._check_before(value, right)
            if not rc:
                return False, self._swap(value, v, update)

            rc, v = self._check_after(value, left)
            if not rc:
                return False, self._swap(value, v, update)

        return True, update

    def _order_update(self, update):
        while True:
            rc, update = self._check_and_swap(update)
            if rc:
                break

        return update

    def soln(self):
        part_1 = 0
        part_2 = 0
        for update in self.updates:
            if self._check_update(update):
                part_1 += update[len(update) // 2]

            else:
                ordered = self._order_update(update)
                part_2 += ordered[len(ordered) // 2]

        print(f"Day 05 Part 1: {part_1}")
        print(f"Day 05 Part 2: {part_2}\n")


class Day6:
    def __init__(self, fd) -> None:
        lines = Path(fd).read_text().strip().split("\n")

        self.nrows = len(lines)
        self.ncols = len(lines[0])

        self.obstacles = {
            (x, y)
            for y in range(self.nrows)
            for x in range(self.ncols)
            if lines[y][x] in "#"
        }

        self.visited = {
            (x, y, "^")
            for y in range(self.nrows)
            for x in range(self.ncols)
            if lines[y][x] in "^"
        }
        self.start = list(self.visited)[0]

    def walk(self, x, y, state, obstacles):
        h = x
        j = y

        match state:
            case "^":
                j -= 1
                ns = ">"

            case ">":
                h += 1
                ns = "v"

            case "v":
                j += 1
                ns = "<"

            case "<":
                h -= 1
                ns = "^"

            case _:
                raise RuntimeError(f"Invalid state: {state}")

        # Can't move, change direction only
        if (h, j) in obstacles:
            return x, y, ns

        # Move in current direction by one
        else:
            return h, j, state

    # Calculate the locations of all possible new obstacles by selecting a
    # a spot directly in front of where the guard would be
    def _calc_obs_locations(self):
        ret = set()
        sx, sy, _ = self.start
        for x, y, state in self.visited:
            match state:
                case "^":
                    h = x
                    j = y - 1

                case ">":
                    h = x + 1
                    j = y

                case "v":
                    h = x
                    j = y + 1

                case "<":
                    h = x - 1
                    j = y

                case _:
                    raise RuntimeError(f"Invalid state: {state}")

            # NOTE: Always skip the starting position, positions off the map, and existing obstacles
            if (
                0 <= h < self.ncols
                and 0 <= j < self.nrows
                and (h, j) != (sx, sy)
                and (h, j) not in self.obstacles
            ):
                ret.add((h, j))

        return list(ret)

    # Part 2, since we know all visited spots and the guard's state in that spot,
    # we can brute force this by placing an obstacle in front of the guard in every
    # possible position and check if this creates a loop.
    def _part_2_func(self, oxoy):
        x, y, state = self.start
        obstacles = self.obstacles | {oxoy}
        visted = {(x, y): 1}

        # print(f"D: Checking {oxoy}")
        while True:
            x, y, state = self.walk(x, y, state, obstacles=obstacles)
            if 0 <= x < self.ncols and 0 <= y < self.nrows:
                if (x, y) in visted:
                    visted[(x, y)] += 1

                else:
                    visted[(x, y)] = 1

            else:
                break

            if visted[(x, y)] > 100:
                return 1

        return 0

    def _part_2_serial(self):
        return sum([self._part_2_func(oxoy) for oxoy in self._calc_obs_locations()])

    def _part_2_parallel(self):
        with Pool(processes=16) as pool:
            result = pool.map(
                func=self._part_2_func,
                iterable=self._calc_obs_locations(),
            )

        return sum(result)

    def soln(self):
        part_1 = 0
        part_2 = 0

        # Part 1, execute walk program and record set of visited positions
        x, y, state = self.start
        while True:
            x, y, state = self.walk(x, y, state, obstacles=self.obstacles)
            if 0 <= x < self.ncols and 0 <= y < self.nrows:
                self.visited.add((x, y, state))

            else:
                break

        part_1 = len({(x, y) for x, y, _ in self.visited})
        # part_2 = self._part_2_serial()
        part_2 = self._part_2_parallel()

        print(f"Day 06 Part 1: {part_1}")
        print(f"Day 06 Part 2: {part_2}\n")


class Day7:
    def __init__(self, fd) -> None:
        self.calibrations = {}
        for line in Path(fd).read_text().strip().split("\n"):
            test, expr = line.split(":")
            self.calibrations[int(test)] = list(map(int, expr.strip().split()))

    def _masks_iter(self, n):
        fmt = f"0{n}b"
        for i in range(2**n):
            yield format(i, fmt)

    def gather_ops(self, n_operands):
        n = n_operands - 1
        return [
            mask.replace("0", "+").replace("1", "*") for mask in self._masks_iter(n)
        ]

    def _concat_masks_iter(self, n):
        for mask in self._masks_iter(n):
            yield mask.replace("1", "|")

    # Sprinkling in the new || op is easy, we don't need the original ops since
    # we only use these for failed tests
    # NOTE: Use '|' instead of '||'
    # FIXME: This still results in a few dups
    def permute_with_concat_op(self, ops_iter):
        ret = []
        n = len(ops_iter[0])
        for ops in ops_iter:
            for mask in self._concat_masks_iter(n):
                new = ""
                for i, c in enumerate(mask):
                    if c == "|":
                        new += c

                    else:
                        new += ops[i]

                ret.append(new)

        return ret

    def check_ops(self, test, expr, ops_iter):
        for ops in ops_iter:
            acc = expr[0]
            for op, opr in zip(ops, expr[1:]):
                match op:
                    case "+":
                        acc += opr

                    case "*":
                        acc *= opr

                    case "|":
                        acc = int(f"{acc}{opr}")

                    case _:
                        raise RuntimeError(f"Invalid op {op}")

                if acc > test:
                    break

            if test == acc:
                return True

        return False

    def _run(self, test, expr):
        part_1 = 0
        part_2 = 0

        ops = self.gather_ops(len(expr))
        if self.check_ops(test, expr, ops):
            part_1 += test

        # Part 2, check only failed tests using the new concat op
        else:
            if self.check_ops(test, expr, self.permute_with_concat_op(ops)):
                part_2 += test

        return part_1, part_1 + part_2

    def _serial(self):
        results = []

        # Part 1, iterate through all exprs and check all possible combinations of operators
        n = 1
        nn = len(self.calibrations)
        for test, expr in self.calibrations.items():
            print(f"D: Checking {n}/{nn}")
            results.append(self._run(test, expr))
            n += 1

        part_1 = 0
        part_2 = 0
        for i, j in results:
            part_1 += i
            part_2 += j

        return part_1, part_2

    def _parallel(self):
        with Pool(processes=16) as pool:
            results = pool.starmap(
                func=self._run,
                iterable=list(self.calibrations.items()),
            )

        part_1 = 0
        part_2 = 0
        for i, j in results:
            part_1 += i
            part_2 += j

        return part_1, part_2

    def soln(self):
        # part_1, part_2 = self._serial()
        part_1, part_2 = self._parallel()

        print(f"Day 07 Part 1: {part_1}")
        print(f"Day 07 Part 2: {part_2}\n")


class Day8:
    def __init__(self, fd):
        self.lines = Path(fd).read_text().strip().split("\n")

        self.nrows = len(self.lines)
        self.ncols = len(self.lines[0])

        self.antennas = {}
        for y in range(self.nrows):
            for x in range(self.ncols):
                if (c := self.lines[y][x]) != ".":
                    if c not in self.antennas:
                        self.antennas[c] = []

                    self.antennas[c].append((x, y))

    def debug(self, antinodes):
        for y in range(self.nrows):
            d = ""
            for x in range(self.ncols):
                if (x, y) in antinodes:
                    d += "#"

                else:
                    d += self.lines[y][x]

            print(d)

    def soln(self):
        part_1 = part_2 = 0

        # Part 1, solve by iterating through the combinations of same-freq antennas
        # Get the dx, dy between pairs and use this to place antinodes
        p1_antinodes = set()
        p2_antinodes = set()
        for antennas in self.antennas.values():
            for (ax, ay), (bx, by) in combinations(antennas, 2):
                dx = bx - ax
                dy = by - ay
                for cx, cy in [(bx + dx, by + dy), (ax - dx, ay - dy)]:
                    if 0 <= cx < self.ncols and 0 <= cy < self.nrows:
                        p1_antinodes.add((cx, cy))

                # Part 2, continuously apply dx, dy in both directions
                # until outside the map for each antenna in the pair
                cx, cy = (bx + dx, by + dy)
                while 0 <= cx < self.ncols and 0 <= cy < self.nrows:
                    p2_antinodes.add((cx, cy))
                    cx += dx
                    cy += dy

                cx, cy = (bx - dx, by - dy)
                while 0 <= cx < self.ncols and 0 <= cy < self.nrows:
                    p2_antinodes.add((cx, cy))
                    cx -= dx
                    cy -= dy

                cx, cy = (ax + dx, ay + dy)
                while 0 <= cx < self.ncols and 0 <= cy < self.nrows:
                    p2_antinodes.add((cx, cy))
                    cx += dx
                    cy += dy

                cx, cy = (ax - dx, ay - dy)
                while 0 <= cx < self.ncols and 0 <= cy < self.nrows:
                    p2_antinodes.add((cx, cy))
                    cx -= dx
                    cy -= dy

        part_1 = len(p1_antinodes)
        part_2 = len(p2_antinodes)

        # self.debug(p2_antinodes)

        print(f"Day 08 Part 1: {part_1}")
        print(f"Day 08 Part 2: {part_2}\n")


def main():
    Day1("inputs/day1.txt").part_1().part_2()
    Day2("inputs/day2.txt").part_1().part_2()
    Day3("inputs/day3.txt").part_1().part_2()
    Day4("inputs/day4.txt").soln()
    Day5("inputs/day5.txt").soln()
    Day6("inputs/day6.txt").soln()
    Day7("inputs/day7.txt").soln()
    Day8("inputs/day8.txt").soln()


if __name__ == "__main__":
    main()
