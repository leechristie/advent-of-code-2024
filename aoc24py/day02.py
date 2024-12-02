# Advent of Code 2024
# Dr Lee A. Christie
#
# GitHub:   @leechristie
# Mastodon: @0x1ac@techhub.social
# Website:  leechristie.com


import time
from collections.abc import Iterable


def reports() -> Iterable[list[int]]:
    with open('input02.txt') as file:
        for line in file:
            line = line.strip()
            yield [int(e) for e in line.split()]


def is_safe(report: list[int]) -> bool:
    diffs = [second - first for first, second in zip(report, report[1:])]
    if max(diffs) > 3 or min(diffs) < -3:
        return False
    if 0 in diffs:
        return False
    signs = [(1 if d > 0 else -1) for d in diffs]
    if 1 in signs and -1 in signs:
        return False
    return True


def unsafe_report_is_repairable(report: list[int]) -> bool:
    for i in range(len(report)):
        if is_safe(report[:i] + report[i + 1:]):
            return True
    return False


def day02() -> None:

    start: float = time.perf_counter()

    part1 = 0
    part2 = 0
    for report in reports():
        if is_safe(report):
            part1 += 1
            part2 += 1
        else:
            if unsafe_report_is_repairable(report):
                part2 += 1

    stop: float = time.perf_counter()

    print("Advent of Code 2024")
    print("Day 2 - Red-Nosed Reports")
    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")
    print(f"Time Taken: {stop-start:.6f} s")
