#!/usr/bin/env python

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

        print(f"Day 01 Part 2: {score}")

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

        print(f"Day 02 Part 2: {self._part_1_safe + n_safe}")
        return self


def main():
    Day1("inputs/day1.txt").part_1().part_2()
    Day2("inputs/day2.txt").part_1().part_2()


if __name__ == "__main__":
    main()
