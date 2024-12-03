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
    increase = False
    decrease = False
    for i in range(len(report) - 1):
        j = i + 1
        first = report[i]
        second = report[j]
        diff = second - first
        if diff == 0 or diff > 3 or diff < -3:
            return False
        elif diff > 0:
            if decrease:
                return False
            increase = True
        else:
            if increase:
                return False
            decrease = True
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
