#!/usr/bin/env python

RED_LIMIT = 12
GREEN_LIMIT = 13
BLUE_LIMIT = 14


class Record:
    def __init__(self, record):
        cl = [c.strip() for c in record.split(",")]
        self._red = 0
        self._blue = 0
        self._green = 0

        for c in cl:
            value, color = [e.strip() for e in c.split(" ")]
            value = int(value)
            if "red" == color:
                self._red = value

            elif "blue" == color:
                self._blue = value

            elif "green" == color:
                self._green = value

            else:
                raise RuntimeError()

    @property
    def colors(self):
        return (self.red, self.blue, self.green)

    @property
    def red(self):
        return self._red

    @property
    def blue(self):
        return self._blue

    @property
    def green(self):
        return self._green

    def is_possible(self):
        return (
            self._red <= RED_LIMIT
            and self._blue <= BLUE_LIMIT
            and self._green <= GREEN_LIMIT
        )

    def __str__(self):
        return "    red: {}, blue {}, green {}, valid: {}".format(
            self._red, self._blue, self._green, self.is_possible()
        )


class Game:
    def __init__(self, i, records):
        self._i = int(i)
        self._records = []

        rl = [r.strip() for r in records.split(";")]
        for r in rl:
            self._records.append(Record(r))

    def is_possible(self):
        for r in self._records:
            if not r.is_possible():
                return False

        return True

    def fewest_cubes(self):
        reds = []
        blues = []
        greens = []
        for r in self._records:
            reds.append(r.red)
            blues.append(r.blue)
            greens.append(r.green)

        return (max(reds), max(blues), max(greens))

    def power(self):
        r, b, g = self.fewest_cubes()
        return r * b * g

    @property
    def number(self):
        return self._i

    def __str__(self):
        ret = "Game {}\n".format(self.number)
        for r in self._records:
            ret += str(r)
            ret += "\n"

        ret += "    is_possible: {}".format(self.is_possible())

        return ret


def part_1():
    with open("./day2.txt") as fd:
        lines = fd.readlines()

    games = []
    for result in lines:
        game, records = [x.strip() for x in result.split(":")]
        _, num = game.split(" ")
        games.append(Game(num, records))

    ans = 0
    ans2 = 0
    for g in games:
        if g.is_possible():
            ans += g.number

        ans2 += g.power()

    print("Part_1: ", ans)
    print("Part_2: ", ans2)


if __name__ == "__main__":
    part_1()
