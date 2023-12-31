import time
from pathlib import Path

import regex as re

schematic = []


def part1(schematic: list[str]):
    symbols: list[tuple[int, int]] = []
    width = len(schematic[0])
    height = len(schematic)

    for i, line in enumerate(schematic):
        for j, char in enumerate(line):
            if char.isdigit() == False and char != ".":
                symbols.append((i, j))

    filtered: list[tuple[int, int]] = []
    sum = 0
    for i, line in enumerate(schematic):
        spans = []

        for r in re.finditer(r"\d+", line):
            spans = r.spans() if r else []
            for span in spans:
                start, end = span
                adj: list[tuple[int, int]] = []
                for x in range(start - 1, end + 1):
                    adj.append((i - 1, x))
                    adj.append((i + 1, x))
                adj.append((i, start - 1))
                adj.append((i, end))

                filtered = [
                    a
                    for a in adj
                    if (
                        a[0] >= 0
                        and a[0] < width - 1
                        and a[1] >= 0
                        and a[1] < height - 1
                    )
                ]

                if any(n in filtered for n in symbols):
                    sum += int(r[0])

    return sum


def part2(schematic: list[str]):
    gears = []
    for i, line in enumerate(schematic):
        for j, char in enumerate(line):
            if char == "*":
                gears.append((i, j))

    sum = 0
    adj: dict[tuple, list[int]] = {}
    for i, line in enumerate(schematic):
        spans = []
        for r in re.finditer(r"\d+", line):
            num: int = int(r[0])
            spans = r.spans() if r else []
            for span in spans:
                start, end = span

                for x in range(start - 1, end + 1):
                    top, bot = (i - 1, x), (i + 1, x)
                    value = adj.get(top)
                    if value:
                        adj.update({top: value + [num]})
                    else:
                        adj.update({top: [num]})

                    value = adj.get(bot)
                    if value:
                        adj.update({bot: value + [num]})
                    else:
                        adj.update({bot: [num]})

                left, right = (i, start - 1), (i, end)
                value = adj.get(left)
                if value:
                    adj.update({left: value + [num]})
                else:
                    adj.update({left: [num]})

                value = adj.get(right)
                if value:
                    adj.update({right: value + [num]})
                else:
                    adj.update({right: [num]})

    for gear in gears:
        pos = adj.get(gear)
        if pos and len(pos) == 2:
            sum += pos[0] * pos[1]

    return sum


def main():
    input = Path(__file__).parent / f"../inputs/{Path(__file__).stem}.txt"
    # input = Path(__file__).parent / f'../inputs/test_{Path(__file__).stem}.txt'
    file = open(input, "r", encoding="utf-8")

    for line in file:
        line = line.strip()
        schematic.append(line)

    p1 = part1(schematic)
    p2 = part2(schematic)
    return (p1, p2)


if __name__ == "__main__":
    t = time.perf_counter_ns()
    (p1, p2) = main()
    elapsed = time.perf_counter_ns() - t
    print(p1, p2)
    print("elapsed: {}s".format(elapsed / 1000000000))
