#!/usr/bin/env python

import re
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


def main():
    Day1("inputs/day1.txt").part_1().part_2()
    Day2("inputs/day2.txt").part_1().part_2()
    Day3("inputs/day3.txt").part_1().part_2()
    Day4("inputs/day4.txt").soln()
    Day5("inputs/day5.txt").soln()


if __name__ == "__main__":
    main()
