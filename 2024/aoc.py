#!/usr/bin/env python

from pathlib import Path


class Day1:
    def __init__(self, fd):
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


def main():
    Day1("inputs/day1.txt").part_1().part_2()


if __name__ == "__main__":
    main()
