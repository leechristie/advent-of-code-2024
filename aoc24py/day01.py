# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


from collections import Counter
import time
from collections.abc import Iterable


def pairs() -> Iterable[tuple[[int, int]]]:
    with open('input01.txt') as file:
        for line in file:
            line = line.strip()
            line = [int(e) for e in line.split()]
            l, r = line
            yield l, r


def day01() -> None:

    start: float = time.perf_counter()

    left: list[int] = []
    right: list[int] = []
    for l, r in pairs():
        left.append(l)
        right.append(r)

    left.sort()
    right.sort()

    r_counts: Counter[int] = Counter(right)

    part1: int = 0
    part2: int = 0
    for l, r in zip(left, right):
        part1 += abs(l - r)
        part2 += l * r_counts[l]

    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 1 - Historian Hysteria")
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print(f"Time Taken: {stop-start:.6f} s")
