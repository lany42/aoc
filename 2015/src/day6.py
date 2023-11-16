from pathlib import Path

ROW_LEN = 1000


def flatten(x, y):
    return (y * ROW_LEN) + x


def collect(p1, p2):
    for y in range(p1[1], p2[1] + 1):
        for x in range(p1[0], p2[0] + 1):
            yield flatten(x, y)


def toggle(idx, lights):
    for i in idx:
        lights[i] += 2


def turn_off(idx, lights):
    for i in idx:
        lights[i] -= 1
        if lights[i] <= 0:
            lights[i] = 0


def turn_on(idx, lights):
    for i in idx:
        lights[i] += 1


def day6():
    lights = [0 for _ in range(1_000 * 1_000)]
    lines = [line for line in Path("./inputs/day6.txt").read_text().split("\n") if line]
    pairs = []
    modes = []

    for line in lines:
        pairs.append(
            [
                (int(x), int(y))
                for x, y in [
                    pair.split(",") for pair in [s for s in line.split() if "," in s]
                ]
            ]
        )

        if "turn on" in line:
            modes.append(turn_on)

        elif "turn off" in line:
            modes.append(turn_off)

        elif "toggle" in line:
            modes.append(toggle)

        else:
            raise RuntimeError()

    for mode, pairs in zip(modes, pairs):
        mode([i for i in collect(*pairs)], lights)

    # print(len([l for l in lights if l]))
    print(sum(lights))


if __name__ == "__main__":
    day6()
